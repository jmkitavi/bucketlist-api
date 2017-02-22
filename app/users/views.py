""" app/users/views"""
from flask import Flask
from flask_restful import Api, Resource, reqparse


class RegistrationAPI(Resource):
    """ User Registration
            -register user"""

    def __init__(self):
        pass

    def post(self):
        """ Register new user"""
        pass


class LoginAPI(Resource):
    """ User Login
            -login user"""
    def __init__(self):
        pass

    def post(self):
        """ Login User"""
        pass

