import unittest
from app.database import Database
from pymongo import MongoClient
from bson.objectid import ObjectId

'''
Slow test running against a real database. Observe that it remove the database at the end. 
'''
class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        # self.client = MagicMock()
        self.client = MongoClient()
        self.db = Database(self.client)

    def test_message_save(self):
        id = ObjectId()
        result = self.db.save_message({'_id': id, 'message': 'msg'})
        self.assertEqual(id, result)

    def test_should_get_message(self):
        id = ObjectId()
        message = {'_id': id, 'message': 'msg'}
        self.db.save_message(message)
        result = self.db.get_message(id)
        self.assertEqual(message, result)

    def test_message_delete(self):
        id = ObjectId()
        self.db.save_message({'_id': id, 'message': 'msg'})
        result = self.db.delete_message(id)
        self.assertEqual(result, 1)

    def tearDown(self):
        """teardown ALL messages in db"""
        self.client.message_db.messages.delete_many({})


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
