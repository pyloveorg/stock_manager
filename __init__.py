__author__ = 'StockManager_Crew'

# import configparser
from config_deployment import DB
from database import db
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from os import path
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.mapper import configure_mappers
import sqlalchemy as sa
from sqlalchemy_searchable import make_searchable



def init_admin():
    user = User()
    user.username = "admin"
    user.password = generate_password_hash('admin', method='sha256')
    user.email = 'admin@gmail.com'
    user.admin = True
    user.poweruser = True
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        print('W bazie istnieje już użytkownik o nazwie: '+user.username)

app = Flask(__name__)
app.static_path = path.join(path.abspath(__file__), 'static')

# config = configparser.ConfigParser()
# config.read('config.ini')
# app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']['SQLALCHEMY_DATABASE_URI']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLALCHEMY_DATABASE_URI'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/stock_manager'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nibzquvhrbkley:228d0b2cb8da271731b2af1978e9666f5e875fb7b38d1aa91213a9f2264b6043@ec2-79-125-12-27.eu-west-1.compute.amazonaws.com:5432/d2t6dujcbf3e53'

app.config['SQLALCHEMY_DATABASE_URI'] = DB.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = DB.SECRET_KEY

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['DB']['SQLALCHEMY_TRACK_MODIFICATIONS']
# app.config['SECRET_KEY'] = config['DB']['SECRET_KEY']



Bootstrap(app)

db.init_app(app)
make_searchable(db.metadata)



with app.test_request_context():
    # if not database_exists(config['DB']['SQLALCHEMY_DATABASE_URI']):
    #     create_database(config['DB']['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(DB.SQLALCHEMY_DATABASE_URI):
        create_database(DB.SQLALCHEMY_DATABASE_URI)
    from auth.models import User, WorkingTimeRecord, LeaveApplication
    from invoices.models import Products, Customers, Invoices, Basket, Quantities, Suppliers, Orders
    sa.orm.configure_mappers()
    db.create_all()
    db.session.commit()
    if not User.query.filter_by(username='admin').first():
        init_admin()


from home.views import home_blueprint
from auth.views import auth_blueprint
from invoices.views import invoices_blueprint
from stock.views import stock_blueprint


app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(invoices_blueprint)
app.register_blueprint(stock_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
   app.run(debug=True)





