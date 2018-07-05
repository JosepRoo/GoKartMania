from flask import session
from passlib.hash import pbkdf2_sha512
from app import Response
import re
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('reservation'):
            return f(*args, **kwargs)
        else:
            return Response(message="Uso de variable de sesion no autorizada.").json(), 401
    return wrap


#utility class used thorughout other classes to perform common functions that dont fit in any other class
class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def mean(arr):
        """
        Calculates the mean value from a list or tuple
        :param arr: [1,2,4,5]
        :return 6
        """
        if arr:
            return sum(arr)/len(arr)
        return 0.0
