from flask_api import FlaskAPI
from instance.config import app_config
from flask import request, jsonify, abort
from app.models import MessageFactory
from app.database import Database
from pymongo import MongoClient


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    message_factory = MessageFactory(app.config["SECRET"])
    db = Database(MongoClient(app.config["DATABASE_URI"]))

    @app.route('/messages/<user_id>/<message_id>', methods=['GET', 'DELETE'])
    def message(user_id, message_id):
        if request.method == "GET":
            message = db.get_message(message_id)
            if message != None:
                return message
            else:
                abort(404)
        else:
            count = db.delete_message(message_id)
            if count == 1:
                response = jsonify()
                response.status_code = 204
                return response
            else:
                abort(404)

    @app.route('/messages/<user_id>', methods=['POST', 'GET'])
    def messages(user_id):  # TODO Validate user_id
        if request.method == "POST":
            user_input = str(request.data.get('message', ''))  # TODO Validate user_input
            message = message_factory.create(user_id, user_input)
            id = db.save_message(message)
            response = jsonify(id=id)
            response.status_code = 201
            return response
        else:
            messages = db.get_messages(user_id)
            if messages != 0:
                return messages
            else:
                abort(404)  # Not sure if I should return 404 or 204

    @app.route('/status', methods=['GET'])
    def status():
        return (jsonify(db.status()))

    return app
