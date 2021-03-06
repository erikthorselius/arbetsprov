from pymongo.errors import ConnectionFailure
import logging


class Database:
    def __init__(self, client):
        self.client = client
        self.db = client.message_db
        self.messages = self.db.messages
        self.id_filter = {'_id': 0}

    def status(self):
        try:
            self.client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            logging.error('MongoDB not available')
            return False

    def save_message(self, message):
        self.messages.insert_one(message)
        return message['id']

    def get_messages(self, user_id, message_ids):
        return list(self.messages.find({'user_id': user_id, 'id': {'$in': message_ids}}, projection=self.id_filter))

    def delete_messages(self, user_id, message_ids):
        return self.messages.delete_many({'id': {'$in': message_ids}, 'user_id': user_id}).deleted_count

    def get_unread_messages(self, user_id):
        query = {'user_id': user_id, 'is_unread': True}
        unread = list(self.messages.find(query, projection=self.id_filter))
        self.messages.update_many(query, {'$set': {'is_unread': False}})
        return unread

    def get_all(self, user_id):
        return list(self.messages.find({'user_id': user_id}, projection=self.id_filter))

    def get_messages_between(self, user_id, start, stop):
        return list(self.messages.find({'user_id': user_id,
                                        'received_datetime': {'$gte': start, '$lt': stop}
                                        }, projection=self.id_filter))
