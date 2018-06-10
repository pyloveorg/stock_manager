import configparser
from auth.models import User
from invoices.models import Products, Customers, Invoices, Basket, Quantities, Suppliers
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash
import sqlalchemy as sa
from sqlalchemy.orm.mapper import configure_mappers
from database import db





def new_stock(name, group, stock_quantity, price, supplier_id):

    """
    products_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(30), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.suppliers_id'), nullable=False)
    ordering = db.relationship('Invoices', secondary=customer_orders, backref=db.backref('invoicing'), lazy='dynamic')
    sup_ordering = db.relationship('Orders', secondary=sup_orders, backref=db.backref('ordering'), lazy='dynamic')
    product_qty = db.relationship('Quantities', backref='product', lazy=True)
    """
    product1 = Products(
        name=name,
        group=group,
        stock_quantity=stock_quantity,
        price=price,
        supplier_id=supplier_id
    )

    db.create_all()
    db.session.add(product1)
    db.session.commit()


if __name__ == '__main__':

    from __init__ import app
    sa.orm.configure_mappers()
    app.app_context().push()
    db.create_all()
    new_stock(ame, group, stock_quantity, price, supplier_id)
