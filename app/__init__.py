# -*- coding: utf-8 -*-
"""
Simple API
~~~~~~~~~~

"""

import datetime as _dt
import os as _os

import bson as _bson
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
        """ Studies list handler """
        if _flask.request.method == 'GET':
            return get_studies(get_db(), user=_flask.request.args.get('user'))
        elif _flask.request.method == 'POST':
            return create_studies(get_db())

    @app.route('/submissions/', methods=['GET'])
    def submissions():
        """ Submissions for study handler"""
        args = _flask.request.args
        return get_submissions(
            get_db(), study=args.get('study'), user=args.get('user'))

    @app.route('/submission/<study_id>', methods=['POST'])
    def submit(study_id):
        """ Study submission handler """
        if _flask.request.is_json:
            request_data = _flask.request.get_json()
            db = get_db()
            study = None

            try:
                study = db.studies.find_one(dict(_id=_bson.ObjectId(study_id)))
            except _mongo.errors.InvalidId:
                pass

            if not study:
                return _flask.jsonify(
                    dict(data=[dict(records=0,
                                    reason='Study not found.')])), 404

            if request_data.get('data') and \
                    valid_submission(request_data.get('data')):
                return create_submission(
                    db, study, request_data.get('data'))

        return _flask.jsonify(
            dict(data=[dict(records=0, reason='Invalid request')])), 400

    def get_db():
        """ Return mongo db """
        client = _mongo.MongoClient(app.config['MONGO_HOST'], 27017)
        return client.get_database('research')

    return app


def get_studies(db, user=None):
    """ Query mongo for list of studies """
    if user:
        query = dict(user=user)
    else:
        query = dict()
    studies = dict(
        data=[to_dict(study) for study in db.studies.find(query)])
    return _flask.jsonify(studies)


def get_submissions(db, study=None, user=None):
    """ Query mongo for list of submissions for a user or study """
    if study and user:
        return _flask.jsonify(
            dict(data=dict(reason='Specify user or study, not both.')))

    if not (study or user):
        return _flask.jsonify(
            dict(data=dict(reason='Specify user or study.')))

    if study:
        try:
            oid = _bson.ObjectId(oid=study)
            query = dict(study=oid)
        except _bson.errors.InvalidId:
            return _flask.jsonify(dict(data=[]))

    elif user:
        query = dict(user=user)

    submissions = dict(
        data=[to_dict(submission, fields=('_id', 'study'))
              for submission in db.submissions.find(query)])

    return _flask.jsonify(submissions)


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
    """ Insert a study into mongo
    >>> create_study(None, {})
    0
    """
    if valid_study(record):
        db.studies.insert(record)
        return 1
    return 0


def create_submission(db, study, record):
    """ Insert a submission into mongo """
    if not has_remaining_places(db, study):
        return _flask.jsonify(
            dict(data=[dict(records=0, reason='Study is full.')])), 400
    try:
        db.submissions.insert(
            dict(user=record['user'], created_at=_dt.datetime.now(),
                 study=_bson.ObjectId(oid=study['_id'])))
        return _flask.jsonify(dict(data=[dict(records=1)]))

    except _mongo.errors.DuplicateKeyError:
        return _flask.jsonify(
            dict(data=[dict(records=0,
                            reason='Only one submission for a study is '
                                   'allowed per user.')])), 400


def valid_study(record):
    """ Check if a record is valid
    >>> valid_study(None)
    False
    >>> valid_study([])
    False
    >>> valid_study(dict())
    False
    >>> valid_study(dict(a='123'))
    False
    >>> valid_study(dict(user='123', available_places=123, name='123', foo=3))
    False
    >>> valid_study(dict(user=123, available_places=123, name='123'))
    False
    >>> valid_study(dict(user='123', available_places='123', name='123'))
    False
    >>> valid_study(dict(user='123', available_places=123, name=123))
    False
    >>> valid_study(dict(user='123', available_places=123, name='123'))
    True
    """
    if not isinstance(record, dict) or \
            set(record.keys()) != {'available_places', 'name', 'user'} or \
            not isinstance(record['available_places'], int) or \
            not isinstance(record['name'], str) or \
            not isinstance(record['user'], str):
        return False

    return True


def valid_submission(record):
    """ Check if a record is valid
    >>> valid_submission(None)
    False
    >>> valid_submission([])
    False
    >>> valid_submission(dict())
    False
    >>> valid_submission(dict(a='123'))
    False
    >>> valid_submission(dict(user='123', bar='bar'))
    False
    >>> valid_submission(dict(user=123))
    False
    >>> valid_submission(dict(user='123'))
    True
    """
    if not isinstance(record, dict) or \
            set(record.keys()) != {'user'} or \
            not isinstance(record['user'], str):
        return False

    return True


def has_remaining_places(db, study):
    """ Check if study has remaining submissions """
    num_submissions = db.submissions.count(dict(study=study['_id']))
    return study['available_places'] > num_submissions


def to_dict(obj, fields=('_id',)):
    """ Transform mongo document to serializable dict
    >>> item = dict(a=_bson.ObjectId('58110204354f8600145fbedd'), b=123)
    >>> transformed = to_dict(item, fields=('a'))
    >>> transformed['a'] == '58110204354f8600145fbedd'
    True
    >>> transformed['b'] == 123
    True
    """
    return dict(obj, **{key: str(obj[key]) for key in fields})
