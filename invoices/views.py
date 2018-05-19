from flask import render_template, redirect, url_for, request, flash
from datetime import datetime
from invoices.models import Products, Customers, Invoices, Basket, Quantities
from database import db

baseTemplate = 'index.html'

from flask import Blueprint

invoices_blueprint = Blueprint('invoices', __name__, template_folder='templates', static_folder='static')


@invoices_blueprint.route('/invoicing', methods=['GET','POST'])
#@login_required
def customer_select():
    customers = Customers.query.all()

    if request.method == 'POST':
        #Choose customer form:
        if request.form.get('customer_id') or request.form.get('customer_name') or request.form.get('customer_id_list'):
            if request.form.get('customer_id'):
                id = int(request.form.get('customer_id'))
                return redirect(url_for('products_select', id=id))
            elif request.method == 'POST' and request.form.get('customer_name'):
                name = request.form.get('customer_name')
                selected_customer = Customers.query.filter_by(name=name).first()
                id = int(selected_customer.id)
                return redirect(url_for('products_select', id=id))
            elif request.method == 'POST' and request.form.get('customer_id_list'):
                id = int(request.form.get('customer_id_list'))
                return redirect(url_for('products_select', id=id))
            else:
                flash('No such customer in db, try again', 'error')
                return render_template('invoicing.html', customers=customers)
    return render_template('invoicing.html',customers=customers)


@invoices_blueprint.route('/invoicing/customer/<int:id>', methods=['GET','POST'])
#@login_required
def products_select(id):
    products = Products.query.all()
    selected_customer = Customers.query.get_or_404(id)
    if request.method == 'POST':

    # Choose product form:
        if request.form.get('product_id') or request.form.get('product_name') or request.form.get(
                'product_id_list'):
            if request.form.get('product_id'):
                product_id = int(request.form.get('product_id'))
                selected_product = Products.query.get_or_404(product_id)
                existing = Basket.query.filter_by(product_id=selected_product.products_id).first()
                if existing:
                    basket = Basket.query.all()
                else:
                    to_basket = Basket(product_id=selected_product.products_id, product_name=selected_product.name,
                                       product_price=selected_product.price, product_group=selected_product.group,
                                       stock_quantity=selected_product.stock_quantity)
                    db.session.add(to_basket)
                    db.session.commit()
                    basket = Basket.query.all()
                return render_template('invoicing.html', products=products, selected_customer=selected_customer,
                                           basket=basket)

            elif request.form.get('product_id_list'):
                product_id = int(request.form.get('product_id_list'))
                selected_product = Products.query.get_or_404(product_id)
                existing = Basket.query.filter_by(product_id=selected_product.products_id).first()
                if existing:
                    basket = Basket.query.all()
                else:
                    to_basket = Basket(product_id=selected_product.products_id, product_name=selected_product.name,
                                       product_price=selected_product.price, product_group=selected_product.group,
                                       stock_quantity=selected_product.stock_quantity)
                    db.session.add(to_basket)
                    db.session.commit()
                    basket = Basket.query.all()
                return render_template('invoicing.html', products=products, selected_customer=selected_customer,
                                       basket=basket)


            basket = Basket.query.all()
            return render_template('invoicing.html', products=products, selected_customer=selected_customer,
                                   basket=basket)


        #Choosing product quantity
        elif request.form.get('product_qty'):
            selected_qty = request.form.get('product_qty')
            return render_template('test.html', selected_qty=selected_qty)

        #Clean basket
        elif request.form.get('clean'):
            basket = Basket.query.all()
            for product in basket:
                db.session.delete(product)
            db.session.commit()
            return render_template('invoicing.html', products=products, selected_customer=selected_customer)

        #Make invoice
        elif request.form.get('make_invoice'):
            basket = Basket.query.all()
            new_invoice = Invoices(customer=selected_customer)
            for item in basket:
                product_qty = int(request.form.get('product_qty'))
                new_product = Products.query.get_or_404(item.product_id)
                new_invoice.invoicing.append(new_product)
                new_quantity = Quantities(invoice=new_invoice, product=new_product, order_quantity=product_qty)
                db.session.delete(item)
            db.session.commit()
            payment_day = new_invoice.date + datetime.timedelta(days=selected_customer.payment)

            return render_template('invoicing.html', products=products, selected_customer=selected_customer, new_invoice=new_invoice, payment_day=payment_day)


    return render_template('invoicing.html', products=products, selected_customer=selected_customer)


