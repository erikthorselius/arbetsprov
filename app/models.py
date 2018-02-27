from collections import namedtuple
from bson.objectid import ObjectId
from datetime import datetime


class MessageFactory(object):
    @classmethod
    def create(cls, user_id, message):
        now = datetime.now()

        return {'_id': ObjectId(),
                'user_id': user_id,
                'message': message,
                'created_date': now.replace(microsecond=0),
                'is_unread': True}
