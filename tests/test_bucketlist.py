""" tests/test_bucketlst"""
import json
from .test_setup import BaseTest


class TestBucketList(BaseTest):
    """ Test for BucketLists"""

    def test_create_bucketlist(self):
        """ Test creation of new bucketlist."""
        bucketlist = {'title': 'Swimming'}
        response = self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Swimming - bucketlist has been added",
                      response.get_data(as_text=True))

    def test_unauthorized_creation(self):
        """" Test unathorized creation."""
        bucketlist = {'title': 'Swimming'}
        response = self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 401)

    def test_creation_without_title(self):
        """ Test creation without title"""
        bucketlist = {'title': '', 'description': 'Nice bucketlist'}
        response = self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Title can't be empty",
                      response.get_data(as_text=True))

    def test_create_existing_bucketlist(self):
        """ Test creating existing bucketlist."""
        bucketlist = {'title': 'Swimming'}
        # post first time
        self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        # post second time
        response = self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        self.assertEqual(response.status_code, 202)
        self.assertIn("BucketList - Swimming already exists",
                      response.get_data(as_text=True))

    def test_get_one_bucketlist(self):
        """ Testing get for single bucketlist."""
        bucketlist = {'title': 'Swimming'}
        # post first time
        self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        response = self.client.get('/bucketlists/1', headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Swimming", response.get_data(as_text=True))

    def test_get_missing_bucketlist(self):
        """ Testing get for missing bucketlist."""
        response = self.client.get('/bucketlists/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        # response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketList with id 1 not found",
                      response.get_data(as_text=True))

    def test_update_bucketlist(self):
        """ Test updating bucketlist."""
        bucketlist = {'title': 'Swimming'}
        bucketlist_update = {'title': 'Driving', 'description':'Widow killer'}
        self.client.post('/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        response = self.client.put(
            '/bucketlists/1', data=json.dumps(bucketlist_update), headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist with id 1 was updated",
                      response_data['message'])

    def test_update_missing_bucketlist(self):
        """ Test missing bucketlist."""
        bucketlist = {'title': 'Swimming'}
        response = self.client.put(
            '/bucketlists/1', data=json.dumps(bucketlist), headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist with id 1 not found",
                      response_data['error'])

    def test_delete_bucketlist(self):
        """ Test deleting bucketlist."""
        bucketlist = {'title': 'Swimming'}
        response = self.client.post(
            '/bucketlists/', data=json.dumps(bucketlist), headers=self.get_header())
        response = self.client.delete(
            '/bucketlists/1', headers=self.get_header())
        self.assertEqual(response.status_code, 200)

    def test_delete_missing_bucketlist(self):
        """ Test missing bucketlist."""
        response = self.client.delete(
            '/bucketlists/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist with id 1 not found",
                      response_data['error'])
