""" app/bucketlists/views"""
import json
from flask import Flask, g, request, json
from flask_restful import Api, Resource, reqparse, marshal, fields
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

        # checking if parameters are null
        if password == "" or username == "":
            return {'error': "Username or Password can't be empty"}, 400
            #  status code - Bad request

        # testing if a user exists
        if Users.query.filter_by(username=username).first() is not None:
            return {'message': 'user with that username already exists'}, 202
            #  status code - request accepted but not processed

        new_user = Users(username=username, password=password)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': '%s has been succesfully registered' % username}, 201
        # status code - created new resource


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

        # checking if parameters are null
        if password == "" or username == "":
            return {'error': "Username or Password can't be empty"}, 400
            #  status code - Bad request

        # getting user details
        user = Users.query.filter_by(username=username).first()
        # add checking hashed password
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'Authorization': token.decode('ascii')}

        return {'message': 'invalid username or password'}, 401
        # status code - unauthorised, login failed


format_item = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'bucketlist_id': fields.Integer,
    'status': fields.Boolean
}
format_bucketlist = {
    'bucketlist_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer,
    'items': fields.Nested(format_item),
}


class BucketListAPI(Resource):
    decorators = [auth.login_required]
    """ One bucket list
            -view one
            -update one
            -delete one"""

    def get(self, bucketlist_id):
        """ View single bucketlist"""
        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first()

        # check if theres a bucketlist
        if bucketlist:
            return marshal(bucketlist, format_bucketlist), 200
            # status code - ok

        return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404
        # status code - not found

    def put(self, bucketlist_id):
        """ Update a bucketlist"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', location='json')

        user_id = g.user.user_id
        args = self.reqparse.parse_args()

        # testing if the bucketlist with that id exists for this user
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=user_id).first()

        if not bucketlist:
            return {'message': 'Bucketlist with %s id not found' % bucketlist_id}, 404

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'The bucketlist with ID %s was updated' % bucketlist_id}

    def delete(self, bucketlist_id):
        """ Delete a bucketlist"""
        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first()

        # check if theres a bucketlist
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            # 204
            return {'message': 'The bucketlist with ID %s was deleted' % bucketlist_id}
            # status code - request processed, no content returned

        return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404
        # status code - not found


class BucketListsAPI(Resource):
    """create one or view many"""
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help="Task title can't be blank", location='json')
        self.reqparse.add_argument(
            'description', type=str, default="", location='json')
        super(BucketListsAPI, self).__init__()

    def post(self):
        """ New Bucketlist"""
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        user_id = g.user.user_id

        # check if title is null
        if title == "":
            return {'error': "Title can't be empty"}, 400
            # status code - Bad request

        # testing if a bucketlist exists
        if BucketList.query.filter_by(title=title).first() is not None:
            return {'message': 'BucketList with that name already exists'}, 202
            #  status code - request accepted but not processed

        bucketlist = BucketList(
            title=title, description=description, created_by=user_id)
        db.session.add(bucketlist)
        db.session.commit()
        return {'message': '{} - bucketlist has been added succesfully by {}'.format(
            title, g.user.username)}, 201
        # status code - created new resource

    # add pagination
    # add search by name
    def get(self):
        """ View many bucketlists"""

        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(created_by=user_id).all()
        return {'bucketlist': marshal(bucketlist, format_bucketlist)}


class BucketListItemsAPI(Resource):
    """ Create new bucket list item
        viewing many handled in get BucketList"""

    decorators = [auth.login_required]
    def get(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "BucketList with ID {} not found.".format(bucketlist_id)}, 404
            # status code - not found
        bucketlistitems = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id).all()
        if not bucketlistitems:
            return {'message': "No Items created yet"}
        return {'items': marshal(bucketlistitems, format_item)}

    def post(self, bucketlist_id):
        """ New Bucketlist Item"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help="Item name can't be blank", location='json')
        self.reqparse.add_argument('status', type=bool, location='json')

        args = self.reqparse.parse_args()
        item_name = args['item_name']
        status = args['status']
        user_id = g.user.user_id

        # check if title is null
        if item_name == "":
            return {'error': "Item Name can't be empty."}, 400
            # status code - Bad request

        if BucketList.query.filter_by(bucketlist_id=bucketlist_id).first() is None:
            return {'error':'BucketList ID {} not found.'.format(bucketlist_id)}, 404
            # status code - Not found

        # check if item name exists in bucketlist
        if BucketListItems.query.filter_by(item_name=item_name,
                                           bucketlist_id=bucketlist_id).first() is not None:
            return {'error': 'BucketList {} already has item with name {}'.format(
                bucketlist_id, item_name)}, 202
            #  status code - request accepted but not processed

        bucketlist_item = BucketListItems(
            item_name=item_name, bucketlist_id=bucketlist_id, status=status)
        db.session.add(bucketlist_item)
        db.session.commit()
        return {'message': '{} - item has been added succesfully to {} bucketlist'.format(
            item_name, bucketlist_id)}, 201
        # status code - created new resource


class BucketListItemAPI(Resource):
    """ One bucketlist item
            -view item
            -edit item
            -delete item"""

    decorators = [auth.login_required]

    def get(self, bucketlist_id, item_id):
        """ view bucketlist item"""

        # check if bucketlist exists
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "BucketList with ID {} not found.".format(bucketlist_id)}, 404
            # status code - not found

        bucketlistitem = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        # check if theres a bucketlist item
        if bucketlistitem:
            return marshal(bucketlistitem, format_item), 200
            # status code - ok

        return {'error': "BucketListItem with ID {} not found.".format(item_id)}, 404
        # status code - not found

    def put(self, bucketlist_id, item_id):
        """ Update bucketlist item"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help="Item name can't be blank", location='json')
        self.reqparse.add_argument('status', type=bool, location='json')

        args = self.reqparse.parse_args()
        user_id = g.user.user_id

        # check if bucketlist exists
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "BucketList with ID {} not found.".format(bucketlist_id)}, 404
            # status code - not found

        bucketlistitem = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        # check if theres a bucketlist item
        if not bucketlistitem:
            return {'error': 'BucketListItem with ID {} not found.'.format(item_id)}, 404
            # status code - not found

        if args.item_name:
            bucketlistitem.item_name = args.item_name
        if args.status:
            bucketlistitem.status = args.status
        db.session.commit()
        return {'message': 'BucketListItem with ID {} was updated.'.format(item_id)}



    def delete(self, bucketlist_id, item_id):
        """ Delete bucketlist item"""
        # check if theres a bucketlist
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404


        # check if theres a bucketlistitem
        bucketlistitem = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        if not bucketlistitem:
            return {'error': "BucketListItem with id {} not found.".format(item_id)}, 404

        db.session.delete(bucketlistitem)
        db.session.commit()
        return {'message': 'BucketListItem with ID {} was deleted'.format(item_id)}
            # 204 status code - request processed, no content returned

