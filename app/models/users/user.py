from flask import session

from app import Database
from app.common.utils import Utils
from app.models.baseModel import BaseModel
from app.models.users.constants import COLLECTION
from app.models.users.errors import InvalidEmail, UserAlreadyRegisteredError

"""
In this user model the email will be used to identify each user although an _id will be created for each instance of it
"""


class User(BaseModel):
    def __init__(self, email, name, reservations=list(), _id=None):
        super().__init__(_id)
        self.email = email
        self.name = name
        self.reservations = reservations

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, kwargs):
        """
        Registers a new user if the provided email was not found in the existing collection
        :param kwargs: key word arguments that contain the new user information
        :return: user object
        """
        email = kwargs['email']
        if not Utils.email_is_valid(email):
            raise InvalidEmail("El email dado no tiene un formato válido.")
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(**kwargs)
            new_user.save_to_mongo(COLLECTION)
            return new_user
        return user

    @staticmethod
    def login(user_email, user_id):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def update_user(self):
        self.update_mongo(COLLECTION)

    def delete_user(self):
        self.delete_from_mongo(COLLECTION)

    def get_reservations(self):
        pass
