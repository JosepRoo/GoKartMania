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

        .. :quickref: Usuario; Login/Registrar un nuevo usuario

        **Example request**:

        .. sourcecode:: http

            POST /user HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "name": "Josep Romagosa",
                "email": "josepromll@gmail.com"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "2d092ef7044b42708833bb4f7ab71082",
                "email": "josepromll@gmail.com",
                "name": "Josep Romagosa",
                "reservations": [
                    a9d6d83a1ba14eae8b2d791e988ae4f
                ]
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 400 Bad request
            Vary: Accept
            Content-Type: application/json

            {
                "message": "El token de acceso ha expirado, inicie sesión nuevamente",
                "success": false
            }

        :resheader Content-Type: application/json
        :status 200: user login
        :status 400: malformed request

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
            return Response.generic_response(e), 500
