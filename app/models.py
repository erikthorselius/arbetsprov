from datetime import datetime
from hashids import Hashids
from random import randint

class MessageFactory(object):
    def __init__(self, salt):
        self.hashids = Hashids(salt=salt, min_length=8)

    def create(self, user_id, message):
        now = datetime.now()
        return {'id': self.hashids.encode(randint(1, 9999)),
                'user_id': user_id,
                'message': message,
                'created_date': now.replace(microsecond=0),
                'is_unread': True}
