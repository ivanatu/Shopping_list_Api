from flask_testing import TestCase
from app.models import db
from app import shop_api, models
from werkzeug.security import generate_password_hash


class BaseTests(TestCase):
    """Tests for the Shopping List API endpoints """
    test_first_name = "aturinda"
    test_last_name = "ivan"
    test_email = "ivo@ivo.com"
    test_password = "Baron1234"
    test_list = "clothes"
    test_name = "item"
    test_price = "5000"

    def create_app(self):
        return shop_api

    def add_user(self):
        """This is a test user to use during the running of tests"""
        user = models.User(first_name = self.test_first_name,
                           last_name=self.test_last_name,
                           email=self.test_email,
                           password=generate_password_hash(
                               self.test_password))
        db.session.add(user)
        db.session.commit()

    def add_list(self):
        """This is a list user to use during the running of tests"""
        the_list = models.Shopping_list(list=self.test_list,
                                        user_id=1)
        db.session.add(the_list)
        db.session.commit()

    def add_item(self):
        """This is a test list item to use during the running of tests"""
        item = models.Item(name=self.test_name,
                           price=self.test_price,
                           List_id=1)
        db.session.add(item)
        db.session.commit()

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


















