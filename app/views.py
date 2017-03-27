""" app/bucketlists/views"""
from flask import g
from flask_restful import Resource, reqparse, marshal, fields
from flask_httpauth import HTTPTokenAuth
from app.models import Users, BucketList, BucketListItems
from app import db


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

            #  status code - Bad request
            return {'error': "Username or Password can't be empty"}, 400

        # testing if a user exists
        if Users.query.filter_by(username=username).first() is not None:

            #  status code - request accepted but not processed
            return {'message': 'user with that username already exists'}, 202

        new_user = Users(username=username, password=password)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()

        # status code - created new resource
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

        # checking if parameters are null
        if password == "" or username == "":

            #  status code - Bad request
            return {'error': "Username or Password can't be empty"}, 400

        # getting user details
        user = Users.query.filter_by(username=username).first()
        # add checking hashed password
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'Authorization': token.decode('ascii')}

        # status code - unauthorised, login failed
        return {'error': 'invalid username or password'}, 401


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
    # 'items': fields.Nested(format_item),
}


class BucketListAPI(Resource):
    """ One bucket list
            -view one
            -update one
            -delete one"""
    decorators = [auth.login_required]

    def get(self, bucketlist_id):
        """ View single bucketlist"""
        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first()

        # check if theres a bucketlist
        if bucketlist:
            # status code - ok
            return marshal(bucketlist, format_bucketlist), 200
        # status code - not found
        return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404

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
            return {'error': 'Bucketlist with id {} not found'.format(bucketlist_id)}, 404

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'Bucketlist with id {} was updated'.format(bucketlist_id)}

    def delete(self, bucketlist_id):
        """ Delete a bucketlist"""
        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first()

        # check if theres a bucketlist
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            # status code 204 - request processed, no content returned
            return {'message': 'The bucketlist with ID %s was deleted' % bucketlist_id}

        return {'error': "Bucketlist with id {} not found.".format(bucketlist_id)}, 404
        # status code - not found


class BucketListsAPI(Resource):
    """create one or view many
    root of bucketist"""
    decorators = [auth.login_required]

    def post(self):
        """ New Bucketlist"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help="Task title can't be blank", location='json')
        self.reqparse.add_argument(
            'description', type=str, default="", location='json')

        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        user_id = g.user.user_id

        # check if title is null
        if title == "":
            # status code - Bad request
            return {'error': "Title can't be empty"}, 400

        # testing if a bucketlist exists
        if BucketList.query.filter_by(title=title, created_by=user_id).first() is not None:

            #  status code - request accepted but not processed
            return {'message': 'BucketList - {} already exists'.format(title)}, 202

        bucketlist = BucketList(
            title=title, description=description, created_by=user_id)
        db.session.add(bucketlist)
        db.session.commit()

        # status code - created new resource
        return {'message': '{} - bucketlist has been added succesfully by {}'.format(
            title, g.user.username)}, 201

    def get(self):
        """ View many bucketlists"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'page', location="args", type=int, required=False, default=1)
        self.reqparse.add_argument(
            'limit', location="args", type=int, required=False, default=20)
        self.reqparse.add_argument('q', location="args", required=False)

        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        page = args['page']
        limit = args['limit']
        search_word = args['q']

        if limit > 100:
            limit = 100

        if search_word:
            bucketlists = BucketList.query.filter(
                BucketList.created_by == user_id,
                BucketList.title.like('%' + search_word + '%')).paginate(page, limit, False)
            if bucketlists:
                total = bucketlists.pages
                bucketlists = bucketlists.items
                response = {'bucketlists': marshal(bucketlists, format_bucketlist),
                            'pages': total
                            }
                return response
            else:
                return {'message': "Bucketlist with {} not found".format(search_word)}, 404

        bucketlists = BucketList.query.filter_by(created_by=user_id).paginate(
            page=page,
            per_page=limit,
            error_out=False)

        total = bucketlists.pages
        bucketlists = bucketlists.items

        response = {'bucketlists': marshal(bucketlists, format_bucketlist),
                    'pages': total,
                    'url': "http://address/bucketlists/?page=",
                    'search': "http://address/bucketlists/?q="
                    }
        return response


class BucketListItemsAPI(Resource):
    """ Create new bucket list item
        viewing many handled in get BucketList
        root of BucketListItems"""

    decorators = [auth.login_required]

    def get(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            # status code - not found
            return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404
        bucketlistitems = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id).all()
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
            # status code - Bad request
            return {'error': "Item Name can't be empty."}, 400

        if BucketList.query.filter_by(bucketlist_id=bucketlist_id).first() is None:
            # status code - Not found
            return {'error': 'BucketList ID {} not found.'.format(bucketlist_id)}, 404

        # check if item name exists in bucketlist
        if BucketListItems.query.filter_by(item_name=item_name,
                                           bucketlist_id=bucketlist_id).first() is not None:
            #  status code - request accepted but not processed
            return {'error': 'BucketList {} already has item with name {}'.format(
                bucketlist_id, item_name)}, 202

        bucketlist_item = BucketListItems(
            item_name=item_name, bucketlist_id=bucketlist_id, status=status)
        db.session.add(bucketlist_item)
        db.session.commit()
        # status code - created new resource
        return {'message': '{} - item has been added succesfully to bucketlist - {}'.format(
            item_name, bucketlist_id)}, 201


class BucketListItemAPI(Resource):
    """ One bucketlist item
            -view item
            -edit item
            -delete item"""

    decorators = [auth.login_required]

    def get(self, bucketlist_id, item_id):
        """ view bucketlist item"""

        # check if bucketlist exists
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            # status code - not found
            return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404

        bucketlistitem = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        # check if theres a bucketlist item
        if bucketlistitem:
            # status code - ok
            return marshal(bucketlistitem, format_item), 200

        # status code - not found
        return {'error': "BucketListItem with id {} not found.".format(item_id)}, 404

    def put(self, bucketlist_id, item_id):
        """ Update bucketlist item"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help="Item name can't be blank", location='json')
        self.reqparse.add_argument('status', type=bool, location='json')

        args = self.reqparse.parse_args()
        user_id = g.user.user_id

        # check if bucketlist exists
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            # status code - not found
            return {'error': "BucketList with id {} not found.".format(bucketlist_id)}, 404

        bucketlistitem = BucketListItems.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        # check if theres a bucketlist item
        if not bucketlistitem:
            # status code - not found
            return {'error': 'BucketListItem with id {} not found.'.format(item_id)}, 404

        if args.item_name:
            bucketlistitem.item_name = args.item_name
        if args.status:
            bucketlistitem.status = args.status
        db.session.commit()
        return {'message': 'BucketListItem with id {} was updated.'.format(item_id)}

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
        # 204 status code - request processed, no content returned
        return {'message': 'BucketListItem with id {} was deleted'.format(item_id)}, 200
