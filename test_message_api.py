import unittest
from app import create_app
import json
from pprint import pprint
from urllib.parse import urljoin


class MessageApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.message_data = 'message_data'

    def test_message_creation(self):
        username = "username"
        res = self.client().post('/messages/' + username, data={'message': self.message_data})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertGreaterEqual(len(data['id']), 8)

    def test_message_get(self):
        res = self.client().post('/messages/username', data={'message': self.message_data})
        data = json.loads(res.data)
        raw_message = self.client().get('/messages/username/' + data['id'])
        message = json.loads(raw_message.data)
        self.assertEqual(raw_message.status_code, 200)
        self.assertEqual(message['message'], self.message_data)

    def test_message_get_not_found(self):
        raw_message = self.client().get('/messages/username/bogusId')
        self.assertEqual(raw_message.status_code, 404)

    def test_message_delete(self):
        res = self.client().post('/messages/username', data={'message': self.message_data})
        data = json.loads(res.data)
        raw_message = self.client().delete('/messages/username/' + data['id'])
        self.assertEqual(raw_message.status_code, 204)

    def test_message_delete_not_found(self):
        raw_message = self.client().delete('/messages/username/bogusId')
        self.assertEqual(raw_message.status_code, 404)

    def test_get_messages(self):
        m1 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        m2 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        ids = {m1.get('id'), m2.get('id')}
        messages = json.loads(self.client().get('/messages/username').data)
        filtered_res = [message for message in messages if message.get('id') in ids]
        self.assertEqual(len(ids), len(filtered_res))

    def tearDown(self):
        """teardown all initialized variables."""


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
