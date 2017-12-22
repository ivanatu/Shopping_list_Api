import json
from app.tests.test_app import BaseTests


class TestItemsTestCase(BaseTests):

    def test_add_an_item_to_an_existing_list(self):
        """
        Test adding an item to a given shopping list.
        """

        self.add_user()
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

    def test_add_an_item_to_a_non_existing_list(self):
        """
        Test adding an item to a shopping list that doesnt exist
        """

        self.add_user()
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

    def test_view_existing_items_on_an_existing_list(self):
        """
        Test viewing items on an existing shopping list.
        """

        self.add_user()
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

    def test_view_non_existing_items_on_an_existing_list(self):
        """
        Test items that dont exist cant be viewed on a given list
        """

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
            response = self.client.get('/shoppinglists/1/items',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")

    def test_update_an_item_on_an_existing_list(self):
        """
        Test updating an existing item on a given shopping list.
        """

        self.add_user()
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
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "item updated",
                             msg="message key fail")

    def test_update_a_non_existing_item_on_an_existing_list(self):
        """
        Testing trying to update an item that doesnt exist on a
        given shopping list.
        """

        self.add_user()
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
            self.assertEqual(reply['message'], "item does not exist",
                             msg="message key fail")

    def test_update_an_item_on_an_non_existing_list(self):
        """
        Testing trying to update an item that exists but
        the shopping list doesn't exist.
        """

        self.add_user()
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

    def test_delete_an_item_on_an_existing_list(self):
        """
        Test deleting an item on a given shopping list
        """

        self.add_user()
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

    def test_delete_a_non_existing_item_on_an_existing_list(self):
        """
        Testing deleting an item that doesnt exist on a given shopping list.
        """

        self.add_user()
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

    def test_delete_an_existing_item_on_a_non_existing_list(self):
        """
        Testing deleting an item that exists on a shopping list that doesnt exist.
        """

        self.add_user()
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
