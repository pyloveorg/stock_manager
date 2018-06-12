from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
# from forms import LoginForm, SignupForm
from invoices.models import Products, Suppliers
from stock.search_engine import search_engine
from stock.add_product import new_stock

productsTemplate = 'products.html'
stock_blueprint = Blueprint("stock", __name__, template_folder='templates')


def columns_tr(model):
    columns = {}
    product_columns = model.__table__.columns.keys()[:-1]
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
    new_stock(
        name=request.form.get("product_name"),
        group=request.form.get("product_group"),
        stock_quantity=request.form.get("product_quantity"),
        price=request.form.get("product_price"),
        supplier_id=request.form.get("supplier_id")
    )

    return redirect(url_for('stock.stock_view'))
