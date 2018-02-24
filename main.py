__author__ = 'Jacek Kalbarczyk'

from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'DirtySecret'

Bootstrap(app)

#sess = session()
db = SQLAlchemy(app)
#db.app = app
#db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#bcrypt = Bcrypt()
app.static_path = path.join(path.abspath(__file__), 'static')
#app.register_blueprint()


if __name__ == '__main__':
    from views import *
    app.run(debug=True)
