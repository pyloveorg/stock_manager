__author__ = 'StockManager_Crew'

import configparser
from database import db
from main import app
from auth.models import User
from invoices.models import Products, Customers, Invoices, Basket, Quantities, Suppliers
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash
import sqlalchemy as sa

def db_start():
    app.app_context().push()
    db.create_all()
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


def add_supp():
    app.app_context().push()
    db.create_all()
    """    suppliers_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.String(30), nullable=False)
    adress = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Float, default=0)
    """
    supplier1 = Suppliers(
        name='Engine Company',
        nip='35223425525',
        adress="Engine town",
        discount=10.15
    )
    sa.orm.configure_mappers()
    app.app_context().push()

    db.create_all()
    db.session.add(supplier1)
    db.session.commit()


if __name__ == '__main__':
    add_supp()
