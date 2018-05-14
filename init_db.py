__author__ = 'Jacek Kalbarczyk'

from main import db
from auth.models import User
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash

def db_start():
    engine = create_engine('postgresql://postgres:postgres@localhost/stock_manager', convert_unicode=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    db.create_all()
    db.session.commit()

    user = User()
    user.username = "admin"
    user.password = generate_password_hash('admin', method='sha256')
    user.email = 'admin@gmail.com'
    user.admin = True
    user.poweruser = True
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        print('W bazie istnieje już użytkownik o nazwie: '+user.username)



if __name__ == '__main__':
    db_start()
