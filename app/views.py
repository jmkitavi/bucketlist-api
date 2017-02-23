""" app/bucketlists/views"""
from flask import Flask
from flask_restful import Api, Resource, reqparse
from app.models import Users
from app import db


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
        db.session.add(new_user)
        db.session.commit()
        return {'message': '%s has been succesfully registered' % username}, 201


class LoginAPI(Resource):
    """ User Login
            -login user"""

    def __init__(self):
        pass

    def post(self):
        """ Login User"""
        pass


class BucketListAPI(Resource):
    """ One bucket list
            -create one
            -view one
            -update one
            -delete one"""

    def __init__(self):
        pass

    def post(self):
        """ New Bucketlist"""
        return "Posting"

    def get(self, bucketlist_id):
        """ View single bucketlist"""
        pass

    def put(self, bucketlist_id):
        """ Update a bucketlist"""
        pass

    def delete(self, bucketlist_id):
        """ Delete a bucketlist"""
        pass


class BucketListsAPI(Resource):
    """ Many bucket list
            -view them"""

    def __init__(self):
        pass

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
