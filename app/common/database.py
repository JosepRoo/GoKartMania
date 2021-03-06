import os

import pymongo
from bson import CodecOptions

from app.models.dates.constants import MEXICO_TZ

__author__ = 'richogtz'


class Database(object):
    # URI = "mongodb://richogtz:cloudstrifeFF7!@127.0.0.1:27017"
    URI = os.environ.get('MONGODB_URI') or "mongodb://127.0.0.1:27017/GoKartMania"
    # URI = "mongodb://127.0.0.1:27017/GoKartMania"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_database()

    @staticmethod
    def insert(collection, data):
        """

        :param collection:
        :param data:
        :return:
        """
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].with_options(
                    codec_options=CodecOptions(
                        tz_aware=True, tzinfo=MEXICO_TZ)).find(query)

    @staticmethod
    def find_one(collection, query, tz_aware=True):
        if not tz_aware:
            return Database.DATABASE[collection].find_one(query)
        return Database.DATABASE[collection].with_options(
                    codec_options=CodecOptions(
                        tz_aware=True, tzinfo=MEXICO_TZ)).find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def aggregate(collection, queries):
        return Database.DATABASE[collection].aggregate(queries)
