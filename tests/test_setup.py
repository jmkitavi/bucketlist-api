""" tests/test_setup
Initialise Test Cases"""
import json
from flask_testing import TestCase
from app.config import configuration
from app.models import Users
from app import db, app

class BaseTest(TestCase):
    """ Initialising TestCase"""

    def create_app(self, app=app):
        """ Initialize app"""
        app.config.from_object(configuration['testing'])
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        db.create_all()

        # create and add a test user
        kitavi = Users(username='kitavi', password='password')
        db.session.add(kitavi)
        db.session.commit()

    def get_header(self):
        """ Gets token for user authentication"""
        user = {"username": "kitavi", "password": "password"}
        response = self.client.post(
            '/auth/login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        token = response_data.get('Authorization')
        return {"Authorization": "token " + token,
                "Accept": 'application/json',
                "Content-Type": 'application/json',
               }

    def tearDown(self):
        db.drop_all()
