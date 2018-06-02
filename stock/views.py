from sqlite3 import IntegrityError

from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
# from forms import LoginForm, SignupForm
from invoices.models import Products, Suppliers
from database import db
# from sqlalchemy.exc import IntegrityError
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import asc
from flask_login import LoginManager
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import select, cast
from sqlalchemy_searchable import search
from stock.search_engine import search_engine

productsTemplate = 'products.html'
stock_blueprint = Blueprint("stock", __name__, template_folder='templates')


# def search_engine(query):
#     product_list = {"Products":[]}
#     if query:
#         search_results = Products.query.order_by(Products.products_id)
#         search_results = search(search_results, query)
#
#     else:
#         search_results = Products.query.order_by(Products.products_id)
#
#     for r in search_results:
#         product_name = str(r)
#         product_list["Products"].append({"name": product_name[1:-1], "columns": [
#             r.products_id,
#             r.name,
#             r.group,
#             r.stock_quantity,
#             r.price,
#             r.supplier_id
#         ]})
#
#     return product_list


def columns_tr(model):
    columns = {}
    product_columns = model.__table__.columns.keys()
    columns["Columns"] = product_columns
    return columns


@stock_blueprint.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    products_columns = columns_tr(Products)
    if request.method == "POST":
        searched_products = search_engine(query=request.form.get('query'))
        return render_template(productsTemplate, searched_products=searched_products, products_columns=products_columns)


@stock_blueprint.route('/stock', methods=['GET', 'POST'])
@login_required
def stock_view():
    products_columns = columns_tr(Products)
    searched_products = search_engine(query=None)
    suppliers = Suppliers.query.order_by(Suppliers.suppliers_id)

    return render_template(productsTemplate,
                           searched_products=searched_products,
                           products_columns=products_columns,
                           suppliers=suppliers
                           )


@stock_blueprint.route('/stock/add', methods=["POST"])
@login_required
def add_stock():
    new_product = Products(
        name=request.form.get("product_name"),
        group=request.form.get("product_group"),
        stock_quantity=request.form.get("product_quantity"),
        price=request.form.get("product_price"),
        supplier_id=request.form.get("supplier_id")
    )
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('stock.stock_view'))
