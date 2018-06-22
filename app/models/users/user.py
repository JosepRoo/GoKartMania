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
        """
        Attempts to find a user according to the given email
        :param email: The email to be found in the User Collection
        :return: Found User object
        """
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, kwargs):
        """
        Registers a new user if the provided email was not found in the existing collection
        :param kwargs: Key word arguments that contain the new user information
        :return: User object
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
