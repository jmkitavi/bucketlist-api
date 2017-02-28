""" app/models/models"""
import datetime
from sqlalchemy.sql import func
# for hashing password
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)  # for creating tokens
from app import db, app
from .config import configuration  # to import secret key


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=100000):
        s = Serializer(configuration['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(configuration['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = Users.query.get(data['user_id'])
        return user

    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)


class BucketList(db.Model):
    __tablename__ = "bucketlist"
    bucketlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(
        "users.user_id", ondelete='CASCADE'), nullable=False)
    items = db.relationship('BucketListItems',
                            backref='bucketlist',
                            passive_deletes=True)


class BucketListItems(db.Model):
    __tablename__ = "bucketlistitems"
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        "bucketlist.bucketlist_id", ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
