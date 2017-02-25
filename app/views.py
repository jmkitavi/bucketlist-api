""" app/bucketlists/views"""
import json
from flask import Flask, g, request
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPTokenAuth
from app.models import Users, BucketList, BucketListItems
from app import db, api, app
from .config import configuration

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    # authenticate by token
    user = Users.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class RegistrationAPI(Resource):
    """ User Registration
            -register user"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username cannot be blank', location='json')
        self.reqparse.add_argument('password', required=True,
                                   help='password cannot be blank', location='json')
        super(RegistrationAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        # testing if a user exists
        if Users.query.filter_by(username=username).first() is not None:
            return {'message': 'user with that username already exists'}
        new_user = Users(username=username, password=password)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': '%s has been succesfully registered' % username}, 201


class LoginAPI(Resource):
    """ User Login
            -login user"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username cannot be blank', location='json')
        self.reqparse.add_argument('password', required=True,
                                   help='password cannot be blank', location='json')
        super(LoginAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        # testing if a user details are correct
        user = Users.query.filter_by(username=username).first()

        # add checking hashed password
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'Authorization': token.decode('ascii')}
        return {'message': 'invalid username or password'}, 401


class BucketListAPI(Resource):
    """ One bucket list
            -view one
            -update one
            -delete one"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='Title can not be blank', location='json')
        self.reqparse.add_argument('description', type=str)
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='Title can not be blank', location='json')

    # @auth.login_required
    def get(self, bucketlist_id):
        """ View single bucketlist"""
        return {"message": "Posting"}

    def put(self, bucketlist_id):
        """ Update a bucketlist"""
        pass

    def delete(self, bucketlist_id):
        """ Delete a bucketlist"""
        pass


class BucketListsAPI(Resource):
    """ Many bucket list
            -create one
            -view many"""

    def __init__(self):
        pass

    # @auth.login_required
    def post(self):
        """ New Bucketlist"""
        pass

    @auth.login_required
    def get(self):
        """ View many bucketlists"""
        pass


class BucketListItemsAPI(Resource):
    """ Many bucketlist item
            -view item"""

    def __init__(self):
        pass

    def get(self, bucketlist_id):
        """ View many bucketlist items"""
        pass


class BucketListItemAPI(Resource):
    """ One bucketlist item
            -add new item
            -view item
            -edit item
            -delete item"""

    def __init__(self):
        pass

    def post(self):
        """ New bucket list item"""
        pass

    def get(self, bucketlist_id, item_id):
        """ view bucketlist item"""
        pass

    def put(self, bucketlist_id, item_id):
        """ Update bucketlist item"""
        pass

    def delete(self, bucketlist_id, item_id):
        """ Delete bucketlist item"""
        pass
