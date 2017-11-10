from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
#from app import db

import jwt

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(500), unique=True)

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def generate_auth_token(self, expiration=100):
        from views import app
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=expiration),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as ex:
            return str(ex)

    @staticmethod
    def decode_token(token):
        """Decodes token from the authorization header"""
        from views import app
        try:
            # try to decode the token using the secret variable
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # token has expired, return n error string
            return "Expired token. Please login to get new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
                     
        
    def __repr__(self):
        return '<User %r>' % self.username

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Integer)
    List_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id'))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Item %r>' % self.name

class Shopping_list(db.Model):
    __tablename__ = 'shopping_lists'
    id = db.Column(db.Integer, primary_key=True)
    list = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return '<Shopping_list %r>' % self.list

