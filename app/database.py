from pymongo.errors import ConnectionFailure
import logging


class Database:
    def __init__(self, client):
        self.client = client
        self.db = client.message_db
        self.messages = self.db.messages

    def status(self):
        try:
            self.client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            logging.error("MongoDB not available")
            return False

    def save_message(self, message):
        return self.messages.insert_one(message).inserted_id

    def get_message(self, message_id):
        return self.messages.find_one({"_id": message_id})

    def delete_message(self, message_id):
        return self.messages.delete_one({"_id": message_id}).deleted_count

    def get_unread_messages(self, user_id):
        query = {'user_id': user_id, 'is_unread': True}
        unread = list(self.messages.find(query))
        self.messages.update_many(query, {'$set': {'is_unread': False}})
        return unread
