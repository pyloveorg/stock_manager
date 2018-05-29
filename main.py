__author__ = 'StockManager_Crew'

import configparser
from database import db
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from os import path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
app.static_path = path.join(path.abspath(__file__), 'static')

config = configparser.ConfigParser()
config.read('config.ini')
# app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLALCHEMY_DATABASE_URI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['DB']['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SECRET_KEY'] = config['DB']['SECRET_KEY']


Bootstrap(app)

db.init_app(app)

# with app.test_request_context():
#     from auth.models import User
#     from invoices.models import Products, Customers, Invoices, Basket, Quantities
#     db.create_all()

from home.views import home_blueprint
from auth.views import auth_blueprint
from invoices.views import invoices_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(invoices_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# with app.app_context():
#     db.init_app(app)


from auth.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
   app.run(debug=True)

