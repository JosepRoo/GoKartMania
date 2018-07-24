import datetime
import os
import xlsxwriter
import pandas as pd

from flask import session
from passlib.hash import pbkdf2_sha512
from app import Response
import re
from functools import wraps

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
    def generate_password():
        """
        Generates a daily-based password for the super-administrator purposes
        :return: A new encrypted password
        """
        current_date = datetime.datetime.now().strftime("%d%m%y")
        private_key = os.environ.get("GKM_PV_KEY")
        secret_key = private_key + current_date
        return secret_key

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

    @staticmethod
    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get('reservation') or session.get('admin_id'):
                return f(*args, **kwargs)
            else:
                return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        return wrap

    @staticmethod
    def admin_login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get('admin_id'):
                return f(*args, **kwargs)
            else:
                return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        return wrap

    @staticmethod
    def sudo_login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get('sudo'):
                return f(*args, **kwargs)
            else:
                return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        return wrap

    @staticmethod
    def generate_report(arr_dict, path, type):
        # Create a Pandas dataframe from the data.
        data = {key: [item[key] if key in item else 0 for item in arr_dict] for key in arr_dict[-1].keys()}
        df = pd.DataFrame(data)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name=type)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

