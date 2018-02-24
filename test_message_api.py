import unittest
import os
import json
from app import create_app

class BucketlistTestCase(unittest.TestCase):
    """This class represents the message test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.message = {'name': 'Go to Borabora for vacation'}


    def test_message_creation(self):
        """Test API can create a message (POST request)"""
        res = self.client().post('/messages/', data=self.message)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()