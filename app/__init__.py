""" app/__init__"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from config.config import configuration


app = Flask(__name__)
api = Api(app)

app.config.from_object(configuration['default'])
# this adds overhead so disabled
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
from app.views import *

api.add_resource(RegistrationAPI, '/auth/register', endpoint='register')
api.add_resource(LoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketListsAPI, '/bucketlists/', endpoint='bucketlists')
api.add_resource(BucketListAPI, '/bucketlists/<bucketlist_id>',
                 endpoint='bucketlist')
api.add_resource(BucketListItemsAPI,
                 '/bucketlists/<bucketlist_id>/items/', endpoint='bucketlist-item')
api.add_resource(BucketListItemAPI,
                 '/bucketlists/<bucketlist_id>/items/<item_id>', endpoint='bucketlist-items')
