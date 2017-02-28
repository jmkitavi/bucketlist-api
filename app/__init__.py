""" app/__init__"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from .config import configuration


app = Flask(__name__)
api = Api(app)

app.config.from_object(configuration['default'])

# this adds overhead so disabled
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
from app.views import *

# registration
api.add_resource(RegistrationAPI, '/auth/register', endpoint='register')
# login
api.add_resource(LoginAPI, '/auth/login', endpoint='login')

# view many bucketlists
# create bucket list
api.add_resource(BucketListsAPI, '/bucketlists/', endpoint='bucketlists')

# view one bucketlist
api.add_resource(BucketListAPI, '/bucketlists/<bucketlist_id>/',
                 endpoint='bucketlist')

# view many bucketlist items
# create BucketList item
api.add_resource(BucketListItemsAPI,
                 '/bucketlists/<bucketlist_id>/items/', endpoint='bucketlist-items')

# view one bucketlist item
api.add_resource(BucketListItemAPI,
                 '/bucketlists/<bucketlist_id>/items/<item_id>', endpoint='bucketlist-item')
