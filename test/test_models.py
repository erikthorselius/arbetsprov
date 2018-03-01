import unittest
from app.models import MessageFactory


class MessageTestCase(unittest.TestCase):
    def test_message_id_length(self):
        message = MessageFactory("salt").create("username", "message")
        self.assertGreaterEqual(len(message['id']), 8)

    def test_datetime_micro_seconds(self):
        message = MessageFactory("salt").create("username", "message")
        self.assertEqual(message['received_datetime'].microsecond, 0)


if __name__ == "__main__":
    unittest.main()
