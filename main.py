__author__ = 'Jacek Kalbarczyk'

from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

#from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

#sess = session()
db = SQLAlchemy()
db.app = app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'

bcrypt = Bcrypt()
#login_manager.session['username'] = 'Zbik'

app.static_path = path.join(path.abspath(__file__), 'static')
#app.register_blueprint()


if __name__ == '__main__':
    """app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)"""
    from views import *
    app.run(debug=True)
