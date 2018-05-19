from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    db.init_app()
    db.app = app
    db.create_all()
    return app
