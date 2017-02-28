from .test_setup import BaseTest
from app.models import Users
import json


class UserTest(BaseTest):

    def test_login(self):
        """ Test login with correct username and password initialised in setup"""

        user = {"username": "kitavi", "password": "password"}
        response = self.client.post(
            '/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('Authorization', response_data)

    def test_failed_login(self):
        pass

    def test_new_registration(self):
        pass

    def test_user_already_exist(self):
        """ Test registering user with existing username"""

        user = {"username": "kitavi", "password": "password"}
        response = self.client.post(
            '/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        response = self.client.post(
            '/auth/register', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('user with that username already exists',
                      response_data['message'])

