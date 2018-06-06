__author__ = 'Jacek Kalbarczyk'

#from flask_login import UserMixin

# from sqlalchemy import Column
#from sqlalchemy.types import Integer
#from sqlalchemy.types import String
#from sqlalchemy.types import Boolean

from database import db
from datetime import datetime
from sqlalchemy_searchable import SearchQueryMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy_utils.types import TSVectorType


class Customers(db.Model):
    __tablename__ = 'customers'
    customers_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    payment = db.Column(db.Integer, default=0)
    invoices = db.relationship('Invoices', backref='customer', lazy=True)


class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    suppliers_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Float, default=0)
    orders = db.relationship('Orders', backref='supplier', lazy=True)
    products = db.relationship('Products', backref='supplier', lazy=True)


class Basket(db.Model):
    __tablename__ = 'basket'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, unique=True, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_price = db.Column(db.Integer, default=0)
    product_group = db.Column(db.String(30), nullable=False)
    product_quantity = db.Column(db.Integer, default=0)
    stock_quantity = db.Column(db.Integer, default=0)
    product_amount = db.Column(db.Integer, default=0)


customer_orders = db.Table('customer_orders',
                  db.Column('products_id', db.Integer, db.ForeignKey('products.products_id')),
                  db.Column('invoices_id', db.Integer, db.ForeignKey('invoices.invoices_id'))
                  )

sup_orders = db.Table('sup_orders',
                  db.Column('products_id', db.Integer, db.ForeignKey('products.products_id')),
                  db.Column('orders_id', db.Integer, db.ForeignKey('orders.orders_id'))
                  )


class ProductsQuery(BaseQuery, SearchQueryMixin):
    pass


class Products(db.Model):
    query_class = ProductsQuery
    __tablename__ = 'products'
    products_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(30), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.suppliers_id'), nullable=False)
    ordering = db.relationship('Invoices', secondary=customer_orders, backref=db.backref('invoicing'), lazy='dynamic')
    sup_ordering = db.relationship('Orders', secondary=sup_orders, backref=db.backref('ordering'), lazy='dynamic')
    product_qty = db.relationship('Quantities', backref='product', lazy=True)
    search_vector = db.Column(TSVectorType('name', 'group', ))

    # def __repr__(self):
    #     return "Products(products_id={}, name='{}', group='{}', quantity='{}', price='{}'".format(self.products_id, self.name, self.group, self.quantity, self.price)


class Invoices(db.Model):
    __tablename__ = 'invoices'
    invoices_id = db.Column(db.Integer, primary_key=True)
    net = db.Column(db.Integer, default=0)
    tax = db.Column(db.Integer, default=0)
    sum = db.Column(db.Integer, default=0)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customers_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantities = db.relationship('Quantities', backref='invoice', lazy=True)


class Orders(db.Model):
    __tablename__ = 'orders'
    orders_id = db.Column(db.Integer, primary_key=True)
    net = db.Column(db.Integer, default=0)
    sum = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.suppliers_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantities = db.relationship('Quantities', backref='order', lazy=True)
    sent = db.Column(db.Boolean, default=False)


class Quantities(db.Model):
    __tablename__ = 'quantities'
    quantities_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.invoices_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.orders_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.products_id'), nullable=False)
    order_quantity = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Integer, default=0)
