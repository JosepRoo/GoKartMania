from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.admins.admin import Admin as AdminModel
from app.models.reservations.errors import ReservationErrors


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
            return AdminModel.admin_login(data).json(), 200
        except AdminErrors as e:
            return Response(message=e.message).json(), 401


class WhoReserved(Resource):
    @staticmethod
    @Utils.login_required
    def get(date, schedule, turn):
        """
        Find the pilots that reserven in the given date, schedule, and turn
        :return: Pilots array
        """
        try:
            return [pilot.json() for pilot in AdminModel.who_reserved(date, schedule, turn)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
