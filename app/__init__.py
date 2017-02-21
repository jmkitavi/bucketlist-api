""" app/__init__"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from config.config import configuration


app = Flask(__name__)
api = Api(app)

app.config.from_object(configuration['default'])
# this add overhead so disabled
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
