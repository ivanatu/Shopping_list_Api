from flask import Flask
import os
from app.models import db

app = Flask(__name__, template_folder='./templates', static_folder='./static')

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'shopping_list',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_DATABASE_URI'] =

"postgresql://ivan:1234@localhost/shopping_list"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'this-is-my-secret-key'
db.init_app(app)

from app import views
