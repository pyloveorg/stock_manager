from flask_wtf import FlaskForm
from wtforms import StringField, validators, FloatField, IntegerField

class CustomerForm(FlaskForm):
    name = StringField('Customer name', [validators.Length(max=80), validators.InputRequired()])
    nip = StringField('NIP',  [validators.Length(max=30), validators.InputRequired()])
    address = StringField('Address', [validators.Length(max=80), validators.InputRequired()])
    payment = IntegerField('Payment', [validators.InputRequired()])


class SupplierForm(FlaskForm):
    name = StringField('Supplier name', [validators.Length(max=80), validators.InputRequired()])
    nip = StringField('NIP', [validators.Length(max=30), validators.InputRequired()])
    address = StringField('Address', [validators.Length(max=80), validators.InputRequired()])
    discount = FloatField('Discount')
