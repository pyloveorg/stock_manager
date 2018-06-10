from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import LoginForm, SignupForm, UserForm, EditWorkplanForm, LeaveApplicationForm
from auth.models import User, WorkingTimeRecord, LeaveApplication
from database import db
from flask import request
import datetime
import calendar
from sqlalchemy_searchable import search
signupTemplate = 'signup.html'
loginModalTemplate = 'login_modal.html'
loginTemplate = 'login.html'
baseTemplate = 'index.html'
usersTemplate = 'users.html'
workplanTemplate = 'workplan.html'


from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return redirect(url_for('auth.edit_user', user_id=current_user.id))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully as {}'.format(current_user.username), 'success')
                return render_template(baseTemplate)

        flash('Invalid username or password', 'danger')
        # return render_template(loginTemplate, form=form, error=True)
        return render_template(loginTemplate, form=form)

    return render_template(loginTemplate, form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data,
                            email=form.email.data,
                            password=hashed_password,
                            name=form.name.data,
                            address=form.address.data,
                            zip_code=form.zip_code.data,
                            city=form.city.data,
                            phone_no=form.phone_no.data)
                            # birth_date=form.birth_date.data)

            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully', 'success')
            return redirect(url_for('home.index'))
            # return render_template(signupTemplate, form=form, success=True, purpose="signup", action=url_for('auth.signup'), success_message='User added successfully')
        except IntegrityError as e:
            flash('User already exists in database', 'danger')
            return render_template(signupTemplate, form=form, purpose="signup", action=url_for('auth.signup'))
    return render_template(signupTemplate, form=form, purpose="signup", action=url_for('auth.signup'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return render_template(baseTemplate)


@auth_blueprint.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.admin is True:
        if request.method == 'POST':
            query = request.form.get('query')
            user_list = User.query.order_by(User.username)
            user_list = search(user_list, query)
        else:
            user_list = User.query.order_by(User.username).all()
    else:
        user_list = User.query.filter_by(id=current_user.id)
    return render_template(usersTemplate, user_list=user_list)

@auth_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # print(current_user.get_id())
    # print(current_user.admin)
    showadminfield = False
    if current_user.admin and current_user.get_id() != user_id:
        showadminfield = True

    if current_user.admin is False and current_user.id != user_id:
        abort(404)

    user = User.query.filter_by(id=user_id).first()
    form = UserForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.name.data = user.name
        form.email.data = user.email
        form.address.data = user.address
        form.zip_code.data = user.zip_code
        form.city.data = user.city
        form.phone_no.data = user.phone_no
        form.admin.data = user.admin
    elif form.validate_on_submit():
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.address = form.address.data
        user.zip_code = form.zip_code.data
        user.city = form.city.data
        user.phone_no = form.phone_no.data
        if current_user.admin and current_user.get_id() != user_id:
            user.admin = form.admin.data
        db.session.commit()
        flash('User successfully updated', 'success')
        return redirect(url_for('auth.users'))

    return render_template(signupTemplate,
                           form=form,
                           action=url_for('auth.edit_user', user_id=user_id),
                           showadminfield=showadminfield)


class WorkplanDay:
    def __init__(self, year, month, day):
        self.start_hour = -1
        self.stop_hour = -1
        self.leave = False
        self.color = 'text-dark'
        self.date = datetime.date(year, month, day)
        self.weekday = calendar.day_name.__getitem__(self.date.weekday())
        if self.date.weekday() in [5,6]:
            self.color = 'text-danger'

class UserWorkplan:
    # list_of_days = list()
    # year = 2032
    def __init__(self, user_id, month, year):
        self.user_id = user_id
        user = User.query.get_or_404(user_id)
        self.name = user.name
        self.username = user.username
        self.month = month
        self.year = year

        if self.month == 0:
            self.month = datetime.date.today().month
            self.year = datetime.date.today().year

        self.month_name = calendar.month_name.__getitem__(self.month)

        self.cal = calendar.Calendar()
        self.list_of_days = list()
        for day in self.cal.itermonthdates(self.year, self.month):
            if day.month == self.month:
                workday = WorkplanDay(day.year, day.month, day.day)
                existing_record = WorkingTimeRecord.query.filter_by(user_id=self.user_id, date=workday.date).first()
                if existing_record:
                    workday.start_hour = existing_record.start_hour
                    workday.stop_hour = existing_record.stop_hour
                    workday.leave = existing_record.leave

                    if workday.start_hour is None:
                        workday.start_hour = -1
                    if workday.stop_hour is None:
                        workday.stop_hour = -1
                    if workday.leave:
                        workday.color = 'text-primary'
                self.list_of_days.append(workday)

    # def __del__(self):
    #     print(self.year, 'died')


@auth_blueprint.route('/workplan/<int:user_id>/<int:month>/<int:year>', methods=['GET'])
@login_required
def user_workplan(user_id, month, year):
    # print(current_user.get_id())
    if user_id == 0:
        user_id = current_user.get_id()
    userWorkplan = UserWorkplan(user_id, month, year)
    monthlist = list()
    for i in range(1, 13):
        monthlist.append((i, calendar.month_name.__getitem__(i)))

    return render_template('workplan.html', userWorkplan=userWorkplan, monthlist=monthlist)


@auth_blueprint.route('/edit_workplan/<int:user_id>/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
@login_required
def edit_workplan(user_id, year, month, day):
    if current_user.admin is not True:
        abort(404)
    date = datetime.date(year, month, day)
    workingday = WorkingTimeRecord.query.filter_by(user_id=user_id, date=date).first()
    username =  User.query.get_or_404(user_id).name
    form = EditWorkplanForm()
    if request.method == 'GET':
        if workingday:
            form.start_hour.data = workingday.start_hour
            form.stop_hour.data = workingday.stop_hour
            form.leave.data = workingday.leave
    else:
        if form.validate_on_submit():
            if not workingday:
                workingDay = WorkingTimeRecord(user_id=user_id, date=date, start_hour=form.start_hour.data, stop_hour=form.stop_hour.data, leave=form.leave.data)
                db.session.add(workingDay)
            else:
                workingday.start_hour = form.start_hour.data
                workingday.stop_hour = form.stop_hour.data
                workingday.leave = form.leave.data

            db.session.commit()

            flash('Workplan successfully updated', 'success')
            return redirect(url_for('auth.user_workplan', user_id=user_id, year=year, month=month))

    return render_template('workplan_edit.html',
                           form=form,
                           username=username,
                           date=date,
                           action=url_for('auth.edit_workplan', user_id=user_id, year=year, month=month, day=day),
                           action_cancel=url_for('auth.user_workplan', user_id=user_id, year=year, month=month))


@auth_blueprint.route('/clear_workplan/<int:user_id>/<int:year>/<int:month>/<int:day>', methods=['POST'])
@login_required
def clear_workplan(user_id, year, month, day):
    if current_user.admin is not True:
        abort(404)
    date = datetime.date(year, month, day)
    workingday = WorkingTimeRecord.query.filter_by(user_id=user_id, date=date).first()
    if workingday:
        db.session.delete(workingday)
        db.session.commit()
        flash('Workplan successfully updated', 'success')
    return redirect(url_for('auth.user_workplan', user_id=user_id, year=year, month=month))


@auth_blueprint.route('/new_leaveapplication/<int:user_id>', methods=['GET', 'POST'])
@login_required
def new_leave_application(user_id):
    username = User.query.get_or_404(user_id).name
    form = LeaveApplicationForm()

    if form.validate_on_submit():
        leaveapplication = LeaveApplication(user_id=user_id,
                                            start_date=form.start_date.data,
                                            end_date=form.end_date.data,
                                            exclude_weekends=form.exclude_weekends.data)
        # start_date = form.start_date.data
        # end_date = form.end_date.data
        # d = start_date
        # delta = datetime.timedelta(days=1)
        # while d <= end_date:
        #     new_day = LeaveApplicationDay()
        #     new_day.date = d
        #     d += delta

        # leaveapplication.days.append(new_day)
        db.session.add(leaveapplication)
        db.session.commit()

        flash('Leave application successfully added', 'success')
        return redirect(url_for('auth.leave_applications'))

    return render_template('leaveapplication_edit.html',
                           form=form,
                           username=username,
                           action=url_for('auth.new_leave_application', user_id=user_id),
                           action_cancel=url_for('auth.leave_applications'))



class UserLeaveApplication:
    def __init__(self, id, employee_name, start_date, end_date, exclude_weekends, status):
        self.id = id
        self.employee_name = employee_name
        self.no_of_days = self.count_no_of_days(start_date, end_date, exclude_weekends)
        self.id = id
        self.status = status
        self.dates = '{} - {}'.format(str(start_date), str(end_date))

    def count_no_of_days(self, start_date, end_date, exclude_weekends):
        counter = start_date
        delta = datetime.timedelta(days=1)
        days_counter = 0
        while counter <= end_date:
            if exclude_weekends is False or counter.weekday() not in [5, 6]:
                days_counter += 1
            counter += delta
        return days_counter



@auth_blueprint.route('/leave_applications', methods=['GET'])
@login_required
def leave_applications():
    user_id = current_user.get_id()

    status = ['None', 'Rejected', 'Accepted']

    applications = list()

    if current_user.admin is True:
        applications = LeaveApplication.query.order_by(LeaveApplication.start_date).all()
    else:
        applications = LeaveApplication.query.filter_by(user_id=user_id).order_by(LeaveApplication.start_date).all()

    application_list = list()
    for item in applications:
        new_application = UserLeaveApplication(item.id, item.user.name, item.start_date, item.end_date,
                                               item.exclude_weekends, status[item.status+1])
        # new_application.id = item.id
        # new_application.employee_name = item.user.name
        # new_application.no_of_days = (item.end_date-item.start_date).days+1
        # new_application.status = status[item.status+1]

        application_list.append(new_application)

    return render_template('leaveapplications.html', application_list=application_list)


@auth_blueprint.route('/edit_leave_application_status/<int:leave_application_id>/<int:leavestatus>', methods=['POST'])
@login_required
def edit_leave_application_status(leave_application_id, leavestatus):
    if current_user.admin is not True:
        abort(404)

    application = LeaveApplication.query.get_or_404(leave_application_id)
    if application:
        start_date = application.start_date
        end_date = application.end_date
        counter = start_date
        delta = datetime.timedelta(days=1)

        application.status = leavestatus
        while counter <= end_date:
            if application.exclude_weekends is False or counter.weekday() not in [5, 6]:
                workingday = WorkingTimeRecord.query.filter_by(user_id=application.user.id, date=counter).first()
                if not workingday:
                    workingday = WorkingTimeRecord(user_id=application.user.id, date=counter, leave=(leavestatus == 1))
                    db.session.add(workingday)
                else:
                    workingday.leave = (leavestatus == 1)
            counter += delta

        db.session.commit()

        if leavestatus:
            flash('Application accepted', 'success')
        else:
            flash('Application rejected', 'success')

    return redirect(url_for('auth.leave_applications'))






