import unittest
from flask_testing import TestCase
from app.models import db
from app import shop_api, models
import json
from flask import Flask
from werkzeug.security import generate_password_hash


class TestShoppingListAPI(TestCase):
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


    # --------------------------- /auth/register endpoint tests --------------------------------------------------------
    def test_01_register_account(self):
        with self.client:
            response = self.client.post(
                'auth/register',
                content_type='application/json',
                data=json.dumps(
                    dict(
                        first_name = "aturinda",
                        last_name="ivan",
                        email = "ivo@ivo.com",
                        password = "Baron1234")
                )
            )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply['email'], "ivo@ivo.com",
                                        msg="email key fail")
        self.assertEqual(reply['status'], "pass",
                                        msg="status key fail")
        self.assertEqual(reply['message'], "user account created successfully",
                                        msg="message key fail")

    def test_02_register_an_existing_account(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            response = self.client.post(
                'auth/register',
                content_type='application/json',
                data=json.dumps(
                    dict(
                        first_name="aturinda",
                        last_name="ivan",
                        email="ivo@ivo.com",
                        password="Baron1234")
                )
            )
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail",
                             msg="status key fail")
            self.assertEqual(reply['message'], "user email already exists",
                             msg="message key fail")

# --------------------------- /auth/login endpoint tests --------------------------------------------------------

    def test_03_login_with_wrong_credentials(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="igwesdsdsde")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail",
                             msg="status key fail")

    def test_04_login_with_correct_credentials(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email = "ivo@ivo.com",
                                            password = "Baron1234")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "login was successful",
                             msg="message key fail")

# --------------------------- /auth/reset-password endpoint tests --------------------------------------------------------

    def test_06_reset_password_with_wrong_credentials(self):
        self.add_user()
        with self.client:
            response = self.client.post('/auth/login',
                                content_type='application/json',
                                data=json.dumps(dict(
                                    email="ivo@ivo.com",
                                    password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/auth/reset-password',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(email="ivo@ivo.com",
                                                old_password="barongh",
                                                new_password="Baron1234")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail",
                             msg="status key fail")
            self.assertEqual(reply['message'], "wrong email or password "
                                               "or may be user does\'t exist",
                             msg="message key fail")

    def test_07_reset_password_with_correct_credentials(self):
        self.add_user()
        with self.client:
            response = self.client.post('/auth/login',
                                content_type='application/json',
                                data=json.dumps(dict(
                                    email="ivo@ivo.com",
                                    password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/auth/reset-password',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(email="ivo@ivo.com",
                                                old_password="Baron1234",
                                                 new_password="baronivo")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "password was changed successfully",
                             msg="message key fail")

 # --------------------------- /shoppinglists endpoint tests -------------------------------------------

    def test_08_create_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            # you have to be logged in to create a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(
                                                email="ivo@ivo.com",
                                                password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/shoppinglists',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(list="groceries")))
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['id'],
                            msg="id key fail")
            self.assertEqual(reply['list'], "groceries",
                             msg="list key fail")
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "list created successfully",
                             msg="message key fail")

    def test_09_list_not_created(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            # you have to be logged in to create a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(
                                                email="ivo@ivo.com",
                                                password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/shoppinglists',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(list="")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail",
                             msg="status key fail")

    def test_10_view_lists(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(email="ivo@ivo.com",
                                                 password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.get('/shoppinglists',
                                       content_type='application/json',
                                       headers=headers)

            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "lists found",
                             msg="message key fail")

    def test_11_view_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.get('/shoppinglists/1',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['list'], msg="lists key fail")
            self.assertEqual(reply['count'], "1", msg="count key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "list found",
                             msg="message key fail")

    def test_12_view_a_non_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(email="ivo@ivo.com",
                                                 password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.get('/shoppinglists/2000',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['count'], "0", msg="count key fail")
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "list not found",
                             msg="message key fail")

    def test_13_update_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.put('/shoppinglists/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(list="cups")))
            reply = json.loads(response.data.decode())

            self.assertTrue(reply['list'], msg="lists key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "list updated",
                             msg="message key fail")

    def test_14_update_a_non_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.put('/shoppinglists/100',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(list="cups")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "list doesnot exist",
                             msg="message key fail")

    def test_15_delete_an_existing_list(self):
        self.add_user()
        self.add_list()
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.delete('/shoppinglists/1',
                                          content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="message key fail")
            self.assertEqual(reply['message'], "list deleted",
                             msg="message key fail")

    def test_16_delete_an_non_existing_list(self):
        self.add_user()
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.delete('/shoppinglists/1',
                                          content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="message key fail")
            self.assertEqual(reply['message'], "list not deleted",
                             msg="message key fail")

  # --------------------------- /shoppinglists items endpoint tests ----------------------------------------

    def test_17_add_an_item_to_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to create a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/shoppinglists/1/items',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(name="soda",
                                                             price="5000")))
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['item_id'], msg="user_id key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "item added to list",
                             msg="message key fail")

    def test_18_add_an_item_to_a_non_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            # you have to be logged in to create a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/shoppinglists/1/items',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(name="soda",
                                                             price="5000")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "list does not exist",
                             msg="message key fail")

    def test_19_view_existing_items_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        self.add_item()
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}
            response = self.client.get('/shoppinglists/1/items',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass", msg="status key fail")

    def test_20_view_non_existing_items_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}
            response = self.client.get('/shoppinglists/1/items',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")

    def test_21_update_an_item_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        self.add_item()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.put('/shoppinglists/1/items/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(name="item",
                                                            price="5000")))
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['item'], msg="item key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "item updated",
                             msg="message key fail")

    def test_22_update_a_non_existing_item_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.put('/shoppinglists/1/items/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(name="item",
                                                            price="5000")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "item not updated",
                             msg="message key fail")

    def test_23_update_an_item_on_an_non_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        self.add_item()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.put('/shoppinglists/3/items/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(
                                           name="item",
                                           price="5000")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "list does not exist",
                             msg="message key fail")

    def test_24_delete_an_item_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        self.add_item()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.delete('/shoppinglists/1/items/1',
                                          content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "item deleted",
                             msg="message key fail")

    def test_25_delete_a_non_existing_item_on_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.delete('/shoppinglists/1/items/1',
                                          content_type='application/json',
                                          headers=headers)
            reply = json.loads(response.data.decode())

            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "item not found",
                             msg="message key fail")

    def test_26_delete_an_existing_item_on_a_non_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        self.add_item()
        with self.client:
            # you have to be logged in to view a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.delete('/shoppinglists/3/items/1',
                                          content_type='application/json',
                                          headers=headers)
            reply = json.loads(response.data.decode())

            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "list does not exist",
                             msg="message key fail")

    #------------------------------------token testing-----------------------------------------------

    def test_27_calling_any_endpoint_with_no_token(self):
        with self.client:
            response = self.client.get('/shoppinglists',
                                       content_type='application/json')

            reply = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_28_calling_any_endpoint_with_wrong_token(self):
        with self.client:
            # you have to be logged in to view a user details
            token = "SDWFiosdf1.spoajsdf.POISDHnkjsaf823rokn"
            headers = {'Authorization': format(token)}

            response = self.client.get('/shoppinglists',
                                       content_type='application/json',
                                       headers=headers)

            reply = json.loads(response.data.decode())
            #self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertTrue(reply['message'],  msg="message key fail")

    def test_30_input_with_incorrect_characters(self):
        with self.client:
            response = self.client.post(
                'auth/register',
                content_type='application/json',
                data=json.dumps(
                    dict(
                        first_name="123aw",
                        last_name="dsvws90",
                        email="ivo@ivo.comn   ",
                        password="Baron1234")
                )
            )
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")

    def test_31_add_an_existing_list(self):
        self.add_user()  # add this test user because tearDown drops all table data
        self.add_list()
        with self.client:
            # you have to be logged in to create a list
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                             password="Baron1234")))

            reply = json.loads(response.data.decode())
            headers = {'Authorization': format(reply['token'])}

            response = self.client.post('/shoppinglists',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(list="clothes")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")

    def test_32_login_with_non_existing_user(self):
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="igwelsldmfsms6787e")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['error'], "user not found. please register",
                             msg="message key fail")


















