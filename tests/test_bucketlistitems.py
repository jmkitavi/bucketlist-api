import json
from .test_setup import BaseTest


class TestBucketListItems(BaseTest):
    """ Test for BucketLists"""

    def add_bucketlist(self):
        """ Add bucketlist for adding items"""
        post = {'title': 'Swimming'}
        self.client.post('/bucketlists/', data=json.dumps(post),
                         headers=self.get_header())

    def test_create_bucketlist_item(self):
        """ Test creation of new bucketlist item."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Small - item has been added succesfully to bucketlist - 1",
                      response.get_data(as_text=True))

    def test_unauthorized_item_creation(self):
        """" Test unathorized creation."""
        bucketlistitem = {'item_name': 'Small', 'status': False}
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem))
        self.assertEqual(response.status_code, 401)

    def test_creation_without_item_name(self):
        """ Test creation without title"""
        self.add_bucketlist()
        bucketlistitem = {'item_name': '', 'status': False}
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item Name can't be empty",
                      response.get_data(as_text=True))

    def test_creating_existing_bucketlist_item(self):
        """ Test creating existing bucketlist item."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        # post first time
        self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        # post second time
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        self.assertEqual(response.status_code, 202)
        self.assertIn("BucketList 1 already has item with name Small",
                      response.get_data(as_text=True))

    def test_get_one_bucketlist_item(self):
        """ Testing get for single bucketlist item."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        response = self.client.get(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Small", response.get_data(as_text=True))

    def test_get_missing_bucketlist_item(self):
        """ Testing get missing bucketlist item."""
        self.add_bucketlist()
        response = self.client.get(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        self.assertIn("BucketListItem with id 1 not found",
                      response.get_data(as_text=True))

    def test_get_item_in_missing_bucketlist(self):
        """ Testing get item in missing bucketlist."""
        response = self.client.get(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        # response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketList with id 1 not found",
                      response.get_data(as_text=True))

    def test_get_items_in_missing_bucketlist(self):
        """ Testing get items in missing bucketlist."""
        response = self.client.get(
            '/bucketlists/1/items/', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        # response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketList with id 1 not found",
                      response.get_data(as_text=True))

    def test_get_items_bucketlist_with_none(self):
        """ Testing get items for bucketlist without items."""
        self.add_bucketlist()
        response = self.client.get(
            '/bucketlists/1/items/', headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        # response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("No Items created yet",
                      response.get_data(as_text=True))

    def test_get_bucketlist_items(self):
        """ Testing get all bucketlist items."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        # post first time
        self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        response = self.client.get(
            '/bucketlists/1/items/', headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        # response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Small", response.get_data(as_text=True))

    def test_update_bucketlist_item(self):
        """ Test updating bucketlist item."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        bucketlistitem_update = {'item_name': 'Small', 'status': True}

        # post first time
        self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        # post second time
        response = self.client.put(
            '/bucketlists/1/items/1',
            data=json.dumps(bucketlistitem_update),
            headers=self.get_header()
            )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketListItem with id 1 was updated",
                      response_data['message'])

    def test_update_item_in_missing_bucketlist(self):
        """ Test updating item in missing bucketlist."""
        bucketlistitem_update = {'item_name': 'Small', 'status': True}
        response = self.client.put(
            '/bucketlists/1/items/1',
            data=json.dumps(bucketlistitem_update),
            headers=self.get_header()
            )
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketList with id 1 not found",
                      response_data['error'])

    def test_update_missing_bucketlist_item(self):
        """ Test updating missing bucketlist item."""
        self.add_bucketlist()
        bucketlistitem_update = {'item_name': 'Small', 'status': True}
        response = self.client.put(
            '/bucketlists/1/items/1',
            data=json.dumps(bucketlistitem_update),
            headers=self.get_header()
            )
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketListItem with id 1 not found",
                      response_data['error'])


    def test_delete_bucketlist_item(self):
        """ Test deleting bucketlist item."""
        self.add_bucketlist()
        bucketlistitem = {'item_name': 'Small', 'status': False}
        # post first time
        self.client.post(
            '/bucketlists/1/items/', data=json.dumps(bucketlistitem), headers=self.get_header())
        # post second time
        response = self.client.delete(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketListItem with id 1 was deleted",
                      response_data['message'])

    def test_delete_item_in_missing_bucketlist(self):
        """ Test deleting item in missing bucketlist."""
        response = self.client.delete(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketList with id 1 not found",
                      response_data['error'])

    def test_delete_missing_bucketlist_item(self):
        """ Test updating missing bucketlist item."""
        self.add_bucketlist()
        response = self.client.delete(
            '/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("BucketListItem with id 1 not found",
                      response_data['error'])
