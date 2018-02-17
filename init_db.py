__author__ = 'Jacek Kalbarczyk'

from sqlalchemy import create_engine
from main import db, bcrypt
from models import User


def db_start():
    #import pdb; pdb.set_trace()
    create_engine('sqlite:///test.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    user = User()
    user.username = "admin"
    user.password = bcrypt.generate_password_hash('a')
    user.email = 'admin@gmail.com'
    user.admin = True
    user.poweruser = True
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db_start()
