__author__ = 'Jacek Kalbarczyk'

from sqlalchemy import create_engine
from main import db
from models import User
from werkzeug.security import generate_password_hash

def db_start():
    create_engine('sqlite:///test.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    user = User()
    user.username = "admin"
    user.password = generate_password_hash('admin', method='sha256')
    user.email = 'admin@gmail.com'
    user.admin = True
    user.poweruser = True
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db_start()
