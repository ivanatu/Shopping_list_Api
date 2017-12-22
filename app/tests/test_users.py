import json
from app.tests.test_app import BaseTests


class TestAuthTestcase(BaseTests):

    def test_register_account(self):
        """
        Testing registering a new user.
        """
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
        self.assertEqual(reply['email'], "ivo@ivo.com",
                         msg="email key fail")
        self.assertEqual(reply['status'], "pass",
                         msg="status key fail")
        self.assertEqual(reply['message'], "user account created successfully",
                         msg="message key fail")

    def test_register_an_existing_account(self):
        """
        Testing failure to register a user because the user already exists.
        """

        self.add_user()
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

    def test_login_with_wrong_credentials(self):
        """
        Testing logging in with the wrong credentials.
        """

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

    def test_login_with_correct_credentials(self):
        """
        Testing logging in a user with correct credentials
        """

        self.add_user()  # add this test user because tearDown drops all table data
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="Baron1234")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "login was successful",
                             msg="message key fail")

    def test_login_with_non_existing_user(self):
        """
        Testing logging in a user who doesnt exist.
        """

        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(
                                            email="ivo@ivo.com",
                                            password="igwelsldmfsms6787e")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['error'], "user not found. please register",
                             msg="message key fail")

    def test_reset_password_with_wrong_credentials(self):
        """
        Testing resetting password with wrong inputs.
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

    def test_reset_password_with_correct_credentials(self):
        """
        Testing resetting password with the correct inputs.
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

    def test_calling_any_endpoint_with_no_token(self):
        """
        Testing end points with no token.
        """

        with self.client:
            response = self.client.get('/shoppinglists',
                                       content_type='application/json')

            reply = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_calling_any_endpoint_with_wrong_token(self):
        """
        Testing end points with a wrong token.
        """

        with self.client:
            # you have to be logged in to view a user details
            token = "SDWFiosdf1.spoajsdf.POISDHnkjsaf823rokn"
            headers = {'Authorization': format(token)}

            response = self.client.get('/shoppinglists',
                                       content_type='application/json',
                                       headers=headers)

            reply = json.loads(response.data.decode())
            # self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertTrue(reply['message'], msg="message key fail")

    def test_input_with_incorrect_characters(self):
        """
        Testing input with incorrect or special characters.
        """

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
