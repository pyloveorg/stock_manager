__author__ = 'Jacek Kalbarczyk'

from database import db


class User(db.Model):
    """
    User model for reviewers.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), default='')
    password = db.Column(db.String(200), default='')
    name = db.Column(db.String(200), default='')
    address = db.Column(db.String(200), default='')
    zip_code = db.Column(db.String(10), default='')
    city = db.Column(db.String(100), default='')
    phone_no = db.Column(db.String(20), default='')
    birth_date = db.Column(db.Date)
    working_days = db.relationship('WorkingTimeRecord', backref='user', lazy=True)
    leave_applications = db.relationship('LeaveApplication', backref='user', lazy=True)

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # return unicode(self.id)
        return self.id


# Dzien pracy
class WorkingTimeRecord(db.Model):
    __tablename__ = 'working_time_record'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Integer)
    stop_hour = db.Column(db.Integer)
    leave = db.Column(db.Boolean, default=False)
    # leave_application_days_id = db.Column(db.Integer, db.ForeignKey('leave_application_days.id'))


# Wniosek o urlop
class LeaveApplication(db.Model):
    __tablename__ = 'leave_application'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, default=-1)
    exclude_weekends = db.Column(db.Boolean, default=True)
    # days = db.relationship('LeaveApplicationDay', backref='leaveapplication', lazy=True)

#Dni wniosku o urlop
# class LeaveApplicationDay(db.Model):
#     __tablename__ = 'leave_application_days'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     leave_application_id = db.Column(db.Integer, db.ForeignKey('leave_application.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
    # workingday = db.relationship('WorkingTimeRecord', backref='customer', lazy=True)
