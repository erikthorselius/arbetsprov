import unittest
from app import create_app
import json


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
        message = json.loads(raw_message.data)[0]
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

    def test_get_messages_by_ids(self):
        m1 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        m2 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        ids = {m1.get('id'), m2.get('id')}
        messages = json.loads(self.client().get('/messages/username/' + m1.get('id') + ',' + m2.get('id')).data)
        filtered_res = [message for message in messages if message.get('id') in ids]
        self.assertEqual(len(ids), len(filtered_res))

    def test_delete_messages_by_ids(self):
        m1 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        m2 = json.loads(self.client().post('/messages/username', data={'message': self.message_data}).data)
        res = self.client().delete('/messages/username/' + m1.get('id') + ',' + m2.get('id'))
        self.assertEqual(res.status_code, 204)

    def test_message_between_start_stop_not_found(self):
        res = self.client().get('/messages/username?start=2018-01-01T10:11:23&stop=2018-02-01T10:09:01')
        self.assertEqual(res.status_code, 404)

    def test_message_with_faulty_start(self):
        res = self.client().get('/messages/username?start=2018-13-01T10:11:23')
        self.assertEqual(res.status_code, 400)

    def test_message_with_faulty_stop(self):
        res = self.client().get('/messages/username?stop=2018-00-01T10:11:23')
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
