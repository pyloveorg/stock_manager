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
