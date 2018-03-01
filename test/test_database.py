import unittest
from app.database import Database
from pymongo import MongoClient
from app.models import MessageFactory
from datetime import datetime, timedelta

'''
Slow test running against a real database. Observe that it remove the database at the end. 
'''


def generate_message_in_time_and_save(self, time):
    message = self.msg_factory._MessageFactory__create_at_time(self.user_id, "message", time)
    self.db.save_message(message)
    return message


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient()
        self.db = Database(self.client)
        self.msg_factory = MessageFactory("salt")
        self.user_id = "username"

    def test_message_save(self):
        message = self.msg_factory.create(self.user_id, "message")
        id = message['id']
        result = self.db.save_message(message)
        self.assertEqual(id, result)

    def test_get_message(self):
        message = self.msg_factory.create(self.user_id, "message")
        id = message['id']
        self.db.save_message(message)
        result = self.db.get_messages(self.user_id, [id])
        assert result[0].items() <= message.items()

    def test_get_messages(self):
        m1 = self.msg_factory.create(self.user_id, "message 1")
        m2 = self.msg_factory.create(self.user_id, "message 2")
        self.db.save_message(m1)
        self.db.save_message(m2)
        result = self.db.get_messages(self.user_id, [m1.get('id'), m2.get('id')])
        self.assertEqual(2, len(result))

    def test_filter_out_database_id(self):
        message = self.msg_factory.create(self.user_id, "message")
        id = message['id']
        self.db.save_message(message)
        result = self.db.get_messages(self.user_id, [id])
        self.assertEqual('', result[0].get('_id', ''))

    def test_delete_message(self):
        message = self.msg_factory.create(self.user_id, "message")
        id = message['id']
        self.db.save_message(message)
        result = self.db.delete_messages(self.user_id, [id])
        self.assertEqual(result, 1)

    def test_delete_messages(self):
        m1 = self.msg_factory.create(self.user_id, "message 1")
        m2 = self.msg_factory.create(self.user_id, "message 2")
        self.db.save_message(m1)
        self.db.save_message(m2)
        result = self.db.delete_messages(self.user_id, [m1.get('id'), m2.get('id')])
        self.assertEqual(2, result)

    def test_find_unread_message(self):
        for x in range(0, 2):
            self.db.save_message(self.msg_factory.create(self.user_id, "message"))
        self.db.get_unread_messages(self.user_id)
        unread_messages = 4
        for x in range(0, unread_messages):
            self.db.save_message(self.msg_factory.create(self.user_id, "message"))
        res = self.db.get_unread_messages(self.user_id)
        self.assertEqual(len(res), unread_messages)

    def test_find_unread_filter_out_id(self):
        self.db.save_message(self.msg_factory.create(self.user_id, "message"))
        message = self.db.get_unread_messages(self.user_id)
        self.assertEqual('', message[0].get('_id', ''))

    def test_get_all_messages(self):
        for x in range(0, 2):
            self.db.save_message(self.msg_factory.create(self.user_id, "message"))
        messages = self.db.get_all(self.user_id)
        self.assertEqual(len(messages), 2)

    def test_get_all_messages_for_bogus_id(self):
        messages = self.db.get_all("bogus_id")
        self.assertEqual(len(messages), 0)

    def test_get_messages_between_start_and_stop(self):
        today = datetime.today().replace(microsecond=0)
        generate_message_in_time_and_save(self, today - timedelta(days=3))
        generate_message_in_time_and_save(self, today - timedelta(days=2))
        generate_message_in_time_and_save(self, today - timedelta(days=1))
        messages = self.db.get_messages_between(self.user_id, today - timedelta(days=2, hours=23, minutes=59, seconds=59), today - timedelta(days=1))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].get('received_datetime'), today - timedelta(days=2))

    def test_get_messages_between_min_and_max(self):
        today = datetime.today().replace(microsecond=0)
        generate_message_in_time_and_save(self, today - timedelta(days=3))
        generate_message_in_time_and_save(self, today - timedelta(days=2))
        generate_message_in_time_and_save(self, today - timedelta(days=1))
        messages = self.db.get_messages_between(self.user_id, datetime.min, datetime.max)
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[1].get('received_datetime'), today - timedelta(days=2))

    def tearDown(self):
        self.client.message_db.messages.delete_many({})


if __name__ == "__main__":
    unittest.main()
