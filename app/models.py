from app import db
from pprint import pprint


class Messages:
    """This class represents the bucketlist table.

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    """
    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        pprint("save")
        #db.session.add(self)
        #db.session.commit()

    @staticmethod
    def get_all():
        pprint("get_all")

    def delete(self):
        pprint("delete")
        #db.session.delete(self)
        #db.session.commit()

    def __repr__(self):
        return "<Messages: {}>".format(self.name)