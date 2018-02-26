import unittest
from app.models import MessageFactory
from bson.objectid import ObjectId

class MessageTestCase(unittest.TestCase):
    def test_message_id(self):
        message =  MessageFactory.create("username", "message")
        self.assertIsInstance(message['_id'], ObjectId)
    def test_datetime_micro_seconds(self):
        message =  MessageFactory.create("username", "message")
        self.assertEqual(message['created_date'].microsecond, 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
