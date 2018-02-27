import unittest
from app.database import Database
from pymongo import MongoClient
from app.models import MessageFactory

'''
Slow test running against a real database. Observe that it remove the database at the end. 
'''
class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        # self.client = MagicMock()
        self.client = MongoClient()
        self.db = Database(self.client)
        self.msg_factory = MessageFactory("salt")

    def test_message_save(self):
        message = self.msg_factory.create("username", "message")
        id = message['id']
        result = self.db.save_message(message)
        self.assertEqual(id, result)

    def test_should_get_message(self):
        message = self.msg_factory.create("username", "message")
        id = message['id']
        self.db.save_message(message)
        result = self.db.get_message(id)
        self.assertEqual(message, result)

    def test_message_delete(self):
        message = self.msg_factory.create("username", "message")
        id = message['id']
        self.db.save_message(message)
        result = self.db.delete_message(id)
        self.assertEqual(result, 1)

    def test_find_unread_message(self):
        for x in range(0, 2):
            self.db.save_message(self.msg_factory.create("username", "message"))
        self.db.get_unread_messages("username")
        unread_messages = 4
        for x in range(0, unread_messages):
            self.db.save_message(self.msg_factory.create("username", "message"))
        res = self.db.get_unread_messages("username")
        self.assertEqual(len(res), unread_messages)

    def tearDown(self):
        """teardown ALL messages in db"""
        self.client.message_db.messages.delete_many({})


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
