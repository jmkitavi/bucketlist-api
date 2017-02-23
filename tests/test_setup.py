""" tests/test_setup
Initialise Test Cases"""
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

    def tearDown(self):
        db.drop_all()
