import os

SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:abc123@localhost/stock_manager')
SECRET_KEY = os.environ.get('DirtySecret')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('False')

