import json
from .test_app import BaseTests


class TestShoppingListTestCase(BaseTests):


    def test_create_list(self):
        """
        This tests whether a shopping list has been created successfully
        """

        self.add_user()
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

    def test_list_not_created(self):
        """
        This is to test whether a shopping list has not been created.
        """

        self.add_user()
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

    def test_view_lists(self):
        """
        This is to test whether we are able view all the shopping lists.
        """

        self.add_user()
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

    def test_view_an_existing_list(self):
        """
        This is to test whether we are able view an existing lshopping ist.
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

            response = self.client.get('/shoppinglists/1',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['list'], msg="lists key fail")
            self.assertEqual(reply['count'], "1", msg="count key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "list found",
                             msg="message key fail")

    def test_view_a_non_existing_list(self):
        """
        This tests that a user cant see a shopping list that
        has not been created yet.
        """

        self.add_user()
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

    def test_update_an_existing_list(self):
        """
        Test whether we can update an existing shopping list.
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

            response = self.client.put('/shoppinglists/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(dict(list="cups")))
            reply = json.loads(response.data.decode())

            self.assertTrue(reply['list'], msg="lists key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "list updated",
                             msg="message key fail")

    def test_update_a_non_existing_list(self):
        """
         Test the shopping list to be updated doesnot exist.
        """

        self.add_user()
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

    def test_delete_an_existing_list(self):
        """
        Test deleting an existing shopping list.
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

            response = self.client.delete('/shoppinglists/1',
                                          content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="message key fail")
            self.assertEqual(reply['message'], "list deleted",
                             msg="message key fail")

    def test_delete_an_non_existing_list(self):
        """
        Test the shopping list to be deleted doesnot exist.
        """

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

    def test_add_an_existing_list(self):
        """
        Test that a shopping list cannot be added twice by the same user.
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

            response = self.client.post('/shoppinglists',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(dict(list="clothes")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
