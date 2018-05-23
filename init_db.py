__author__ = 'StockManager_Crew'

import configparser
from database import db
from main import app
from auth.models import User
from invoices.models import Products, Customers, Invoices, Basket, Quantities
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash


def db_start():
    config = configparser.ConfigParser()
    config.read('config.ini')

    engine = create_engine(config['DB']['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
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
