from flask import session
from flask_restful import Resource

from app import Response
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.reservations.constants import PARSER, COLLECTION_TEMP
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel


class Reservations(Resource):
    @staticmethod
    def post():
        """
        Registers a new reservation given its type
        :return: JSON object with the created reservation
        """
        try:
            data = PARSER.parse_args()
            return ReservationModel.add(data), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    def put():
        """
        Updates the current reservation given its new type
        :return: JSON object with the updated reservation
        """
        try:
            if session.get('reservation'):
                data = PARSER.parse_args()
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return ReservationModel.update(reservation, data.get('type')).json(), 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
