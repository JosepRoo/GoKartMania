from flask import session

from app import Database
from app.models.baseModel import BaseModel
from app.models.users.constants import COLLECTION

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
