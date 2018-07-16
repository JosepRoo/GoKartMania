from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel


class User(Resource):
    @staticmethod
    @Utils.login_required
    def post():
        """
        Registers a new user manually given its body parameters
        :return: A brand new user, or a session to the currently existing user
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
        data = parser.parse_args()
        try:
            return UserModel.register(data).json(), 200
        except UserErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500
