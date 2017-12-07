from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

#from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_URI2, SECRET_KEY

shop_api = Flask(__name__, template_folder='./templates', static_folder='./static')
TEST = True

shop_api.config['DEBUG'] = True
if os.environ.get('DATABASE_URL'):
    shop_api.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    if TEST:
        shop_api.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI2']
    else:
        shop_api.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

shop_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
shop_api.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(shop_api)
db.init_app(shop_api)

from app import views
