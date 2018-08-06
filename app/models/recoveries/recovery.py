import uuid

from app.models.recoveries.constants import COLLECTION
from app.common.database import Database


class Recovery(object):
    def __init__(self, admin_email, _id=None):
        self.admin_email = admin_email
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        "recovery with id {} for user: {}".format(self._id, self.admin_email)

    def save_to_mongo(self):
        Database.insert(COLLECTION, self.json())

    def remove_from_mongo(self):
        Database.remove(COLLECTION, self.json())

    @classmethod
    def get_recovery(cls, _id=None):
        """
        Fetches a list of the all the Recovery objects in the given collection
        :param _id: The specific ID of a particular collection
        :return: List of Recovery objects or one specific Recovery object
        """
        if _id is None:
            return [cls(**recovery) for recovery in Database.find(COLLECTION, {})]

        else:
            return [cls(Database.find_one(COLLECTION, {'_id': _id}))]

    @classmethod
    def get_recovery_by_email(cls, admin_email):
        """
        Finds the Recovery object with the given user email
        :param admin_email: user object to be updated
        :return: Recovery object
        """
        Database.find_one(COLLECTION, {'admin_email': admin_email})

    def json(self):
        """
        Creates a JSON object with the id and the user email
        :return: JSON object
        """
        return {
            '_id': self._id,
            'admin_email': self.admin_email
        }

    @classmethod
    def recover_in_db(cls, recovery_id):
        """
        Recovers the password in the database with a unique recovery ID
        :param recovery_id: ID to ensure a secure recuperation of the password
        :return: Boolean
        """
        obj_recovery = Database.find_one(COLLECTION, {'_id': recovery_id})
        if obj_recovery is None:
            return False
        else:
            recovery_in_DB = cls(**obj_recovery)
            Database.remove(COLLECTION, {'_id': recovery_id})
            return True
