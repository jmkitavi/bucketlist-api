""" tests/test_users"""
from .test_setup import BaseTest
import json


class UserTest(BaseTest):
    """ Tests for user login and registration"""

    def test_login(self):
        """ Test login with correct username and password initialised in setup"""

        user = {"username": "kitavi", "password": "password"}
        response = self.client.post(
            '/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('Authorization', response_data)

    def test_failed_login(self):
        """ Login with bad credentials."""

        user = {"username": "wrong", "password": "credentials"}
        response = self.client.post(
            '/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'], 'invalid username or password')

    def test_bad_login(self):
        """ Login with bad request"""

        user = {"username": "", "password": "password"}
        response = self.client.post(
            '/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Username or Password can't be empty",
                      response_data['error'])

    def test_new_registration(self):
        """ Creating a new user."""

        user = {"username": "joseph", "password":"password"}
        response = self.client.post(
            'auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('succesfully registered', response_data['message'])

    def test_user_already_exist(self):
        """ Test registering user with existing username"""

        user = {"username": "kitavi", "password": "password"}
        response = self.client.post(
            '/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('user with that username already exists',
                      response_data['message'])

    def test_bad_registration(self):
        """ Test bad request when registering"""

        user = {"username": "", "password": "password"}
        response = self.client.post(
            '/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Username or Password can't be empty",
                      response_data['error'])

