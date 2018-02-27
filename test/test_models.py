import unittest
from app.models import MessageFactory
from bson.objectid import ObjectId

class MessageTestCase(unittest.TestCase):
    def test_message_id_length(self):
        message =  MessageFactory("salt").create("username", "message")
        self.assertGreaterEqual(len(message['id']), 8)
    def test_datetime_micro_seconds(self):
        message =  MessageFactory("salt").create("username", "message")
        self.assertEqual(message['created_date'].microsecond, 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
