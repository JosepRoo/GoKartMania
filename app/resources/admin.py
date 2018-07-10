from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.admins.admin import Admin as AdminModel


class Admin(Resource):
    @staticmethod
    def post():
        """
        Registers a new admin manually given its body parameters
        :return: A brand new admin, or a session to the currently existing admin
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        data = parser.parse_args()
        try:
            if email[email.index('@')+1:] == 'gokartmania.com':

                data = parser.parse_args()
            if data.get('password') == Utils.generate_password():
                return AdminModel.admin_login(data).json(), 200
            else:
                return Response(message="Credenciales incorrectas").json(), 401
        except AdminErrors as e:
            return Response(message=e.message).json(), 401
