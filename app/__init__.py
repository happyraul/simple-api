# -*- coding: utf-8 -*-
"""
Simple API
~~~~~~~~~~

"""

import os as _os

import flask as _flask
import pymongo as _mongo

_env = _os.environ.get


def create_app():
    """ Create a flask app """
    app = _flask.Flask(__name__)
    app.config['MONGO_HOST'] = _env('APP_MONGO_HOST') or 'localhost'
    app.debug = _env('APP_DEBUG') or True

    @app.route('/studies', methods=['POST', 'GET'])
    def studies():
        """ Studies view handler """
        if _flask.request.method == 'GET':
            return get_studies(get_db())
        elif _flask.request.method == 'POST':
            return create_studies(get_db())

    def get_db():
        """ Return mongo db """
        client = _mongo.MongoClient(app.config['MONGO_HOST'], 27017)
        return client.get_database('research')

    return app


def get_studies(db):
    """ Query mongo for list of studies """
    studies = dict(
        data=[to_dict(study) for study in db.studies.find()])
    return _flask.jsonify(studies)


def create_studies(db):
    """ Insert new studies into mongo from request data """
    if _flask.request.is_json:
        request_data = _flask.request.get_json()

        if request_data.get('data') and \
                isinstance(request_data['data'], list):
            records = 0

            for record in request_data.get('data'):
                records += create_study(db, record)

            return _flask.jsonify(dict(data=[dict(records=records)]))

    return _flask.jsonify(
        dict(data=[dict(records=0, reason='Invalid request')])), 400


def create_study(db, record):
    """ Insert a study into mongo """
    if valid_record(record):
        db.studies.insert(record)
        return 1
    return 0


def valid_record(record):
    """ Check if a record is valid """
    if not isinstance(record, dict) or \
            set(record.keys()) != {'available_places', 'name', 'user'} or \
            not isinstance(record['available_places'], int) or \
            not isinstance(record['name'], str) or \
            not isinstance(record['user'], str):
        return False

    return True


def to_dict(obj):
    """ Transform mongo document to serializable dict """
    return dict(obj, _id=str(obj['_id']))
