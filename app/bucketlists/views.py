""" app/bucketlists/views"""
from flask import Flask
from flask_restful import Api, Resource, reqparse

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
        pass

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
    """ One bucketlist item
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
