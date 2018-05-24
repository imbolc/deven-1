import flask.json
from bson import ObjectId
from pymongo import MongoClient

from settings import MONGO_URI


db = MongoClient(MONGO_URI)[MONGO_URI.split('/')[-1]]


class JSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return flask.json.JSONEncoder.default(self, o)
