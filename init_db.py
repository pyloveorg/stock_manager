__author__ = 'Jacek Kalbarczyk'

from sqlalchemy import create_engine
from main import db, bcrypt
import models


def db_start():
    #import pdb; pdb.set_trace()
    create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    user = models.User()
    user.username = "admin"
    user.password = bcrypt.generate_password_hash('admin_password')
    user.email = 'admin@gmail.com'
    user.admin = True
    user.poweruser = True
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db_start()
