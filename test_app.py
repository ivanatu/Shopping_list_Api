import unittest
from app import app, models
from app.models import db
#from flask_testing import TestCase
import json
from werkzeug.security import generate_password_hash

class TestShoppingListAPI(unittest.TestCase):
	def setUp(self):
		self.user = {"first_name":"aturinda", "last_name":"ivan", "username":"ivan", "password":"1234"}
		db.create_all()
		db.session.commit()

	def tearDown(self):
	 	db.session.remove()
	 	db.drop_all()

	def add_user(self):
	 	"""This is a test user to use during the running of tests"""
	 	user = models.User(username=self.test_user,
	 					   password=generate_password_hash(self.test_user_password))
	 	db.session.add(user)
	 	db.session.commit()

	def add_list(self):
		"""This is a list user to use during the running of tests"""
		the_list = models.Shopping_list(user_id=1,
							   list=self.test_list)
		db.session.add(the_list)
		db.session.commit()

	def add_item(self):
		"""This is a test list item to use during the running of tests"""
		item = models.Item(name=self.test_item,
						   List_id=1,
						   price=self.test_item_price)
		db.session.add(item)
		db.session.commit()

	# --------------------------- /auth/register endpoint tests --------------------------------------------------------
	def test_register_account(self):
		with self.client:
			response = self.client().post('/auth/register',
										content_type='application/json',
										data=json.dumps(dict(self.user)))
			reply = json.loads(response.data.decode())
			self.assertEqual(reply['first_name'], "aturinda", msg="first_name key fail")
			self.assertEqual(reply['last_name'], "ivan", msg="last_name key fail")
			self.assertEqual(reply['username'], "ivan", msg="username key fail")
			self.assertEqual(reply['message'], "user created successfully", msg="message key fail")

	def test_register_an_existing_account(self):
		self.add_user()  # add this test user because tearDown drops all table data
		with self.client:
			response = self.client().post('/auth/register',
										content_type='application/json',
										data=json.dumps(dict(self.user)))
			reply = json.loads(response.data.decode())
			self.assertEqual(reply['status'], "fail", msg="status key fail")
			self.assertEqual(reply['message'], "user already exists", msg="message key fail")