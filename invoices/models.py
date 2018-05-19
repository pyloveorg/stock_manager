__author__ = 'Staszek'

from database import db
from datetime import datetime


class Customers(db.Model):
    __tablename__ = 'customers'
    customers_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.String(30), nullable=False)
    adress = db.Column(db.String(80), nullable=False)
    payment = db.Column(db.Integer, default=0)
    invoices = db.relationship('Invoices', backref='customer', lazy=True)

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


orders = db.Table('orders',
                  db.Column('products_id', db.Integer, db.ForeignKey('products.products_id')),
                  db.Column('invoices_id', db.Integer, db.ForeignKey('invoices.invoices_id'))
                  )

class Products(db.Model):
    __tablename__ = 'products'
    products_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(30), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    ordering = db.relationship('Invoices', secondary=orders, backref=db.backref('invoicing'), lazy='dynamic')
    product_qty = db.relationship('Quantities', backref='product', lazy=True)

    def __repr__(self):
        return "Products(products_id={}, name='{}', group='{}', quantity='{}', price='{}'".format(self.products_id, self.name, self.group, self.quantity, self.price)

class Invoices(db.Model):
    __tablename__ = 'invoices'
    invoices_id = db.Column(db.Integer, primary_key=True)
    net = db.Column(db.Integer, default=0)
    tax = db.Column(db.Integer, default=0)
    sum = db.Column(db.Integer, default=0)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customers_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantities = db.relationship('Quantities', backref='invoice', lazy=True)

class Quantities(db.Model):
    __tablename__ = 'quantities'
    quantities_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.invoices_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.products_id'), nullable=False)
    order_quantity = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Integer, default=0)