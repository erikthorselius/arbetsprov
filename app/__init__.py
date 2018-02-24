from flask_api import FlaskAPI
from instance.config import app_config
from flask import request, jsonify, abort
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db=client.admin


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from app.models import Messages
    @app.route('/messages/', methods=['POST', 'GET'])
    def messages():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                message = Messages(name=name)
                message.save()
                response = jsonify({
                    'id': '123',
                    'name': message.name,
                })
                response.status_code = 201
                return response
        else:
            # GET
            messages = Messages.get_all()
            results = []

            for message in messages:
                obj = {
                    'id': message.id,
                    'name': message.name,
                    'date_created': message.date_created,
                    'date_modified': message.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    return app