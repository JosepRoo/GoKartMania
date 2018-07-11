from flask import session
from app import Database
from app.models.baseModel import BaseModel
from app.models.users.constants import COLLECTION

"""
In this user model the email will be used to identify each user although an _id will be created for each instance of it
"""


class Admin(BaseModel):
    def __init__(self, email, name, _id=None):
        super().__init__(_id)
        self.email = email
        self.name = name

    @classmethod
    def get_by_email(cls, email):
        """
        Attempts to find a user according to the given email
        :param email: The email to be found in the Admin Collection
        :return: Found Admin object
        """
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def admin_login(cls, data):
        email = data.get('email')
        admin = Admin.get_by_email(email)
        data.pop('password')
        if admin is None:
            new_admin = cls(**data)
            new_admin.save_to_mongo(COLLECTION)
        else:
            new_admin = cls(**data, _id=admin._id)
            new_admin.update_mongo(COLLECTION)
        session['admin_id'] = new_admin._id
        return new_admin
