from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

shop_api = Flask(__name__, template_folder='./templates', static_folder='./static')
CORS(shop_api)
TEST = False

shop_api.config['DEBUG'] = True
if os.environ.get('DATABASE_URL'):
    shop_api.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    if TEST:
        shop_api.config['SQLALCHEMY_DATABASE_URI2'] = os.environ['SQLALCHEMY_DATABASE_URI2']
    else:
        shop_api.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

shop_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
shop_api.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(shop_api)
db.init_app(shop_api)
shop_api.config['CORS_HEADERS'] = 'Content-Type'



from app import views
