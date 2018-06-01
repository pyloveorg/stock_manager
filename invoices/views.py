from flask import render_template, redirect, url_for, request, flash
from datetime import datetime
from invoices.models import Products, Customers, Invoices, Basket, Quantities, Suppliers
from database import db
from invoices.forms import CustomerForm, SupplierForm
from flask_login import login_required
baseTemplate = 'index.html'

from flask import Blueprint

invoices_blueprint = Blueprint('invoices', __name__, template_folder='templates')


@invoices_blueprint.route('/invoicing', methods=['GET','POST'])
#@login_required
def customer_select():
    customers = Customers.query.all()

    if request.method == 'POST':
        #Choose customer form:
        if request.form.get('customer_id') or request.form.get('customer_name') or request.form.get('customer_id_list'):
            if request.form.get('customer_id'):
                id = int(request.form.get('customer_id'))
                return redirect(url_for('invoices.products_select', id=id))
            elif request.method == 'POST' and request.form.get('customer_name'):
                name = request.form.get('customer_name')
                selected_customer = Customers.query.filter_by(name=name).first()
                id = int(selected_customer.id)
                return redirect(url_for('invoices.products_select', id=id))
            elif request.method == 'POST' and request.form.get('customer_id_list'):
                id = int(request.form.get('customer_id_list'))
                return redirect(url_for('invoices.products_select', id=id))
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
            selected_qty = request.form.get('product_qty').split(' ')
            product_id = int(selected_qty[0])
            product_qty = int(selected_qty[1])
            current_product = Basket.query.filter_by(product_id=product_id).first()
            current_product.product_quantity = product_qty
            current_product.product_amount = current_product.product_price * current_product.product_quantity
            db.session.commit()
            basket = Basket.query.all()
            return render_template('invoicing.html', products=products, selected_customer=selected_customer,
                                   basket=basket)
            #return render_template('test.html', selected_qty=selected_qty, product_id=product_id, product_qty=product_qty, current_product=current_product)

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
            net_sum = 0
            for item in basket:
                product_qty = item.product_quantity
                total_price = item.product_amount
                new_product = Products.query.get_or_404(item.product_id)
                new_invoice.invoicing.append(new_product)
                net_sum += round(float(total_price),2)
                new_quantity = Quantities(invoice=new_invoice, product=new_product, order_quantity=product_qty, total_price=total_price)
                db.session.add(new_quantity)
                db.session.delete(item)
            new_invoice.net = net_sum
            new_invoice.tax = round(float(new_invoice.net * 0.23),2)
            new_invoice.sum = round(float(new_invoice.net + new_invoice.tax),2)
            db.session.add(new_invoice)
            db.session.commit()
            new_invoice = Invoices.query.order_by("-invoices_id").first()
            payment_day = new_invoice.date + datetime.timedelta(days=selected_customer.payment)
            new_invoice.payment_date = payment_day
            db.session.commit()
            new_invoice = Invoices.query.order_by("-invoices_id").first()
            return render_template('invoicing.html', products=products, selected_customer=selected_customer, new_invoice=new_invoice, payment_day=payment_day)


    return render_template('invoicing.html', products=products, selected_customer=selected_customer)

# Invoices Archive

#All invoices
@invoices_blueprint.route('/invoices', methods=['GET','POST'])
#@login_required
def invoices_archive():
    invoices = Invoices.query.all()
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', invoices=invoices)

# Select invoices by customer
@invoices_blueprint.route('/invoices/customer', methods=['GET','POST'])
#@login_required
def invoices_by_customer():
    customers = Customers.query.all()
    if request.method == 'POST':
        #Choose customer form:
        if request.form.get('customer_id') or request.form.get('customer_name') or request.form.get('customer_id_list'):
            if request.form.get('customer_id'):
                id = int(request.form.get('customer_id'))
                return redirect(url_for('invoices.customer_invoices', id=id))
            elif request.method == 'POST' and request.form.get('customer_id_list'):
                id = int(request.form.get('customer_id_list'))
                return redirect(url_for('invoices.customer_invoices', id=id))
            else:
                flash('No such customer in db, try again', 'error')
                return render_template('invoices.html', customers=customers)
    return render_template('invoices.html', customers=customers)

#List of selected customer's invoices
@invoices_blueprint.route('/invoices/customer/<int:id>', methods=['GET','POST'])
#@login_required
def customer_invoices(id):
    selected_customer = Customers.query.get_or_404(id)
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', selected_customer=selected_customer)

# Select invoices by product
@invoices_blueprint.route('/invoices/product', methods=['GET','POST'])
#@login_required
def invoices_by_product():
    products = Products.query.all()
    if request.method == 'POST':

    # Choose product form:
        if request.form.get('product_id') or request.form.get('product_id_list'):
            if request.form.get('product_id'):
                product_id = int(request.form.get('product_id'))
                return redirect(url_for('invoices.product_invoices', product_id=product_id))
            elif request.form.get('product_id_list'):
                product_id = int(request.form.get('product_id_list'))
                return redirect(url_for('invoices.product_invoices', product_id=product_id))
    return render_template('invoices.html', products=products)

#List of selected product's invoices
@invoices_blueprint.route('/invoices/product/<int:product_id>', methods=['GET','POST'])
def product_invoices(product_id):
    selected_product = Products.query.get_or_404(product_id)
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', selected_product=selected_product)


#Selected invoice
@invoices_blueprint.route('/invoice/<int:inv_id>', methods=['GET', 'POST'])
def selected_invoice(inv_id):
    invoice = Invoices.query.get_or_404(inv_id)
    return render_template('invoice.html', invoice=invoice)

@invoices_blueprint.route('/customers', methods=['GET'])
@login_required
def customers():
    customer_list = Customers.query.order_by(Customers.name).all()
    return render_template('customers.html', customer_list=customer_list)


@invoices_blueprint.route('/suppliers', methods=['GET'])
@login_required
def suppliers():
    supplier_list = Suppliers.query.order_by(Suppliers.name).all()
    return render_template('suppliers.html', supplier_list=supplier_list)

@invoices_blueprint.route('/customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customers.query.get_or_404(customer_id)
    form = CustomerForm()
    if request.method == 'GET':
        form.name.data = customer.name
        form.nip.data = customer.nip
        form.address.data = customer.address
    elif form.validate_on_submit():
        customer.name = form.name.data
        customer.nip = form.nip.data
        customer.address = form.address.data
        db.session.commit()
        flash('Customer successfully updated', 'success')
        return redirect(url_for('invoices.customers'))

    return render_template('customer_edit.html',
                           form=form,
                           action=url_for('invoices.edit_customer', customer_id=customer_id),
                           edit_mode=1)

@invoices_blueprint.route('/supplier/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = Suppliers.query.get_or_404(supplier_id)
    form = SupplierForm()
    if request.method == 'GET':
        form.name.data = supplier.name
        form.nip.data = supplier.nip
        form.address.data = supplier.address
        form.discount.data = supplier.discount
    elif form.validate_on_submit():
        supplier.name = form.name.data
        supplier.nip = form.nip.data
        supplier.address = form.address.data
        supplier.discount = form.discount.data
        db.session.commit()
        flash('Supplier successfully updated', 'success')
        return redirect(url_for('invoices.suppliers'))

    return render_template('supplier_edit.html',
                           form=form,
                           action=url_for('invoices.edit_supplier', supplier_id=supplier_id),
                           edit_mode=1)

@invoices_blueprint.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers()
        customer.name = form.name.data
        customer.address = form.address.data
        customer.nip = form.nip.data
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully', 'success')
        return redirect(url_for('invoices.customers'))

    return render_template('customer_edit.html',
                            form=form,
                            action=url_for('invoices.add_customer'),
                            edit_mode=0)

@invoices_blueprint.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Suppliers()
        supplier.name = form.name.data
        supplier.address = form.address.data
        supplier.nip = form.nip.data
        supplier.discount = form.discount.data
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully', 'success')
        return redirect(url_for('invoices.suppliers'))

    return render_template('supplier_edit.html',
                            form=form,
                            action=url_for('invoices.add_supplier'),
                            edit_mode=0)