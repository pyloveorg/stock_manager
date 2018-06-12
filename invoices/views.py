from flask import render_template, redirect, url_for, request, flash
from datetime import datetime

from invoices.models import Products, Customers, Invoices, Basket, Quantities, Suppliers, Orders
from database import db
from flask_weasyprint import HTML, render_pdf, CSS
from flask_mail import Message
from invoices.forms import CustomerForm, SupplierForm
from flask_login import login_required

baseTemplate = 'index.html'

from flask import Blueprint

invoices_blueprint = Blueprint('invoices', __name__, template_folder='templates')


@invoices_blueprint.route('/invoicing', methods=['GET', 'POST'])
@login_required
def customer_select():
    customers = Customers.query.all()

    if request.method == 'POST':
        #Choose customer form:
        try:
            if request.form.get('customer_id') or request.form.get('customer_name') or request.form.get('customer_id_list'):
                if request.form.get('customer_id'):
                    id = int(request.form.get('customer_id'))
                    if Customers.query.get(id):
                        return redirect(url_for('invoices.products_select', id=id))
                    else:
                        flash('No such customer in db, try again', 'danger')
                        return render_template('invoicing.html', customers=customers)
                elif request.method == 'POST' and request.form.get('customer_name'):
                    name = request.form.get('customer_name')
                    try:
                        selected_customer = Customers.query.filter_by(name=name).first()
                        id = int(selected_customer.id)
                    except AttributeError:
                        flash('There is no such customer in db', 'danger')
                        return render_template('invoicing.html', customers=customers)
                    return redirect(url_for('invoices.products_select', id=id))
                elif request.method == 'POST' and request.form.get('customer_id_list'):
                    id = int(request.form.get('customer_id_list'))
                    return redirect(url_for('invoices.products_select', id=id))
                else:
                    flash('No such customer in db, try again', 'danger')
                    return render_template('invoicing.html', customers=customers)
        except ValueError or AttributeError:
            flash('You have to chose correct customer', 'danger')
            return render_template('invoicing.html', customers=customers)
    return render_template('invoicing.html',customers=customers)

@invoices_blueprint.route('/invoicing/customer/<int:id>', methods=['GET','POST'])
@login_required
def products_select(id):
    products = Products.query.all()
    selected_customer = Customers.query.get_or_404(id)
    if request.method == 'POST':

    # Choose product form:

        if request.form.get('product_id') or request.form.get('product_name') or request.form.get(
                'product_id_list'):
            try:
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
            except ValueError:
                flash("You have to choose product!", 'danger')

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


        #Clean basket
        elif request.form.get('clean'):
            basket = Basket.query.all()
            for product in basket:
                db.session.delete(product)
            db.session.commit()
            flash('Basket is empty now', 'success')
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
                if product_qty > 0:
                    new_quantity = Quantities(invoice=new_invoice, product=new_product, order_quantity=product_qty, total_price=total_price)
                    new_product.stock_quantity -= product_qty
                    db.session.add(new_quantity)
                    db.session.delete(item)
                else:
                    flash('You have to choose quantity', 'danger')
                    return render_template('invoicing.html', products=products, selected_customer=selected_customer,
                                           basket=basket)
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
            inv_id = new_invoice.invoices_id

            # Checking product quantities in stock (to make automatic invoice in case of lack of some product)
            all_products = Products.query.all()
            order_dict = {}
            for product in all_products:
                if product.stock_quantity < 2:
                    if product.supplier_id not in order_dict:
                        order_dict[product.supplier_id] = [product.products_id]
                    else:
                        order_dict[product.supplier_id].append(product.products_id)
            if order_dict:
                for supplier in order_dict:
                    new_order = Orders(supplier_id=supplier)
                    db.session.add(new_order)
                    db.session.commit()
                    new_order = Orders.query.order_by("-orders_id").first()
                    order_net = 0
                    for product in order_dict[supplier]:
                        new_product = Products.query.get_or_404(product)
                        total_price = 5 * new_product.price * new_order.supplier.discount
                        order_net += round(float(total_price),2)
                        new_quantities = Quantities(order=new_order, product=new_product, order_quantity=5,
                                                    total_price=total_price)
                        new_order.ordering.append(new_product)
                        db.session.add(new_quantities)
                        db.session.commit()
                    order_sum = round(float(order_net * new_order.supplier.discount), 2)
                    new_order.net = order_net
                    new_order.sum = order_sum
                    db.session.commit()
            flash('Invoice added', 'success')
            return redirect(url_for('selected_invoice', inv_id=inv_id))
    else:
        return render_template('invoicing.html', products=products, selected_customer=selected_customer)

# Invoices Archive

#All invoices
@invoices_blueprint.route('/invoices', methods=['GET','POST'])
@login_required
def invoices_archive():
    invoices = Invoices.query.all()
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', invoices=invoices)

# Select invoices by customer
@invoices_blueprint.route('/invoices/customer', methods=['GET','POST'])
@login_required
def invoices_by_customer():
    customers = Customers.query.all()
    if request.method == 'POST':
        #Choose customer form:
        try:
            if request.form.get('customer_id') or request.form.get('customer_name') or request.form.get('customer_id_list'):
                if request.form.get('customer_id'):
                    id = int(request.form.get('customer_id'))
                    if Customers.query.get(id):
                        return redirect(url_for('invoices.customer_invoices', id=id))
                    else:
                        flash('No such customer in db, try again', 'danger')
                        return render_template('invoices.html', customers=customers)

                elif request.method == 'POST' and request.form.get('customer_id_list'):
                    id = int(request.form.get('customer_id_list'))
                    return redirect(url_for('invoices.customer_invoices', id=id))
        except ValueError:
            flash('Select customer please', 'danger')
            return render_template('invoices.html', customers=customers)
    return render_template('invoices.html', customers=customers)

#List of selected customer's invoices
@invoices_blueprint.route('/invoices/customer/<int:id>', methods=['GET','POST'])
@login_required
def customer_invoices(id):
    selected_customer = Customers.query.get_or_404(id)
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', selected_customer=selected_customer)

# Select invoices by product
@invoices_blueprint.route('/invoices/product', methods=['GET','POST'])
@login_required
def invoices_by_product():
    products = Products.query.all()
    if request.method == 'POST':

    # Choose product form:
        try:
            if request.form.get('product_id') or request.form.get('product_id_list'):
                if request.form.get('product_id'):
                    product_id = int(request.form.get('product_id'))
                    if Products.query.get(product_id):
                        return redirect(url_for('invoices.product_invoices', product_id=product_id))
                    else:
                        flash('No such product in db, try again', 'danger')
                        return render_template('invoices.html', products=products)
                elif request.form.get('product_id_list'):
                    product_id = int(request.form.get('product_id_list'))
                    return redirect(url_for('invoices.product_invoices', product_id=product_id))
        except ValueError:
            flash('You have to chose some product', 'danger')
            return render_template('invoices.html', products=products)
    return render_template('invoices.html', products=products)


#List of selected product's invoices
@invoices_blueprint.route('/invoices/product/<int:product_id>', methods=['GET','POST'])
def product_invoices(product_id):
    selected_product = Products.query.get_or_404(product_id)
    if request.method == 'POST':
        inv_id = request.form.get('selected_invoice')
        return redirect(url_for('invoices.selected_invoice', inv_id=inv_id))
    return render_template('invoices.html', selected_product=selected_product)


#Print order to PDF
def order_print_pdf(ord_id):
    order = Orders.query.get_or_404(ord_id)
    html = render_template('order_pdf.html', order=order)
    order_pdf = HTML(string=html).write_pdf()
    subject = 'Stock manager order no {}'.format(ord_id)
    msg = Message(subject=subject,
                  sender="stockmanager.pylove@gmail.com",
                  recipients=["stockmanager.pylove@gmail.com"])
    msg.body = 'Please find order no {}, for following goods {}, in attachment'.format(ord_id, [part.name for part in order.ordering])

    msg.attach(filename='StockManager_Order_{}.pdf'.format(ord_id), data=order_pdf, content_type="application/pdf")
    mail.send(msg)
    sent_order = Orders.query.get_or_404(ord_id)
    for part in sent_order.ordering:
        part.stock_quantity += 5
        db.session.commit()
    sent_order.sent = True
    db.session.commit()
    return 'Sent'

#Selected invoice
@invoices_blueprint.route('/invoice/<int:inv_id>', methods=['GET', 'POST'])
def selected_invoice(inv_id):
    new_orders = Orders.query.filter_by(sent=False).all()
    invoice = Invoices.query.get_or_404(inv_id)
    if request.method == 'POST':
        if request.form.get('Print'):
            return redirect(url_for('invoices.print_pdf', inv_id=inv_id))
        elif request.form.get('select'):
            ord_id = request.form.get('select')
            return redirect(url_for('invoices.supplier_order', ord_id=ord_id))
        elif request.form.get('send'):
            ord_id = request.form.get('send')
            order_print_pdf(ord_id)
            new_orders = Orders.query.filter_by(sent=False).all()
            flash('Order sent to supplier', 'success')
            return render_template('invoice.html', invoice=invoice, new_orders=new_orders)
    if new_orders: flash('You have to order some products', 'danger')
    return render_template('invoice.html', invoice=invoice, new_orders=new_orders)

#Print invoice to PDF
@invoices_blueprint.route('/invoice_pdf/<int:inv_id>')
def print_pdf(inv_id):
    invoice = Invoices.query.get_or_404(inv_id)
    html = render_template('invoice_pdf.html', invoice=invoice)
    css = CSS(url_for('static', filename='invoice_pdf.css'))
    return render_pdf(HTML(string=html), stylesheets=[css])

#Orders to supplier:
@invoices_blueprint.route('/order/<int:ord_id>', methods=['GET', 'POST'])
@login_required
def supplier_order(ord_id):
    order = Orders.query.get_or_404(ord_id)
    if request.method == 'POST':
        if request.form.get('send'):
            order_print_pdf(ord_id)
            flash('Order sent to supplier', 'success')
            return render_template('order.html', order=order)
    return render_template('order.html', order=order)

#Sent orders
@invoices_blueprint.route('/orders', methods=['GET','POST'])
@login_required
def orders_archive():
    sent_orders = Orders.query.filter_by(sent=True).all()
    if request.method == 'POST':
        ord_id = request.form.get('selected_order')
        return redirect(url_for('invoices.supplier_order', ord_id=ord_id))
    new_orders = Orders.query.filter_by(sent=False).all()
    if new_orders: flash('You have to order some products', 'danger')
    return render_template('orders.html', sent_orders=sent_orders)

#Orders to send
@invoices_blueprint.route('/orders/to_order', methods=['GET','POST'])
@login_required
def to_order():
    new_orders = Orders.query.filter_by(sent=False).all()
    if request.form.get('select'):
        ord_id = request.form.get('select')
        return redirect(url_for('invoices.supplier_order', ord_id=ord_id))
    elif request.form.get('send'):
        ord_id = request.form.get('send')
        order_print_pdf(ord_id)
        new_orders = Orders.query.filter_by(sent=False).all()
        return render_template('orders.html', new_orders=new_orders)
    if not new_orders: flash('You dont need to send any order now', 'success')
    return render_template('orders.html', new_orders=new_orders)

# Select orders by supplier
@invoices_blueprint.route('/orders/supplier', methods=['GET','POST'])
@login_required
def orders_by_supplier():
    suppliers = Suppliers.query.all()
    if request.method == 'POST':
        #Choose supplier form:
        try:
            if request.form.get('supplier_id') or request.form.get('supplier_id_list'):
                if request.form.get('supplier_id'):
                    id = int(request.form.get('supplier_id'))
                    if Suppliers.query.get(id):
                        return redirect(url_for('invoices.supplier_orders', id=id))
                    else:
                        flash('No such supplier in db, try again', 'danger')
                        return render_template('orders.html', suppliers=suppliers)
                elif request.method == 'POST' and request.form.get('supplier_id_list'):
                    id = int(request.form.get('supplier_id_list'))
                    return redirect(url_for('invoices.supplier_orders', id=id))
        except ValueError:
            flash('Select supplier please', 'danger')
            return render_template('orders.html', suppliers=suppliers)
    return render_template('orders.html', suppliers=suppliers)

#List of selected supplier's orders
@invoices_blueprint.route('/orders/supplier/<int:id>', methods=['GET','POST'])
@login_required
def supplier_orders(id):
    selected_supplier = Suppliers.query.get_or_404(id)
    if request.method == 'POST':
        if request.form.get('select'):
            ord_id = request.form.get('select')
            return redirect(url_for('invoices.supplier_order', ord_id=ord_id))
    return render_template('orders.html', selected_supplier=selected_supplier)

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
        form.payment.data = customer.payment
    elif form.validate_on_submit():
        customer.name = form.name.data
        customer.nip = form.nip.data
        customer.address = form.address.data
        customer.payment = form.payment.data
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
        customer.payment = form.payment.data
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
