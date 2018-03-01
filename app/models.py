from datetime import datetime
from hashids import Hashids
from random import randint


class MessageFactory(object):
    def __init__(self, salt):
        self.hashids = Hashids(salt=salt, min_length=8)

    def __create_at_time(self, user_id, message, received_datetime):
        return {'id': self.hashids.encode(randint(1, 9999)),
                'user_id': user_id,
                'message': message,
                'received_datetime': received_datetime.replace(microsecond=0),
                'is_unread': True}

    def create(self, user_id, message):
        return self.__create_at_time(user_id, message, datetime.now())
