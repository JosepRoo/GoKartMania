from flask import session
from flask_restful import Resource

from app import Response
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.reservations.constants import PARSER, COLLECTION_TEMP, PROMO
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
from app.common.utils import Utils


class Reservations(Resource):
    @staticmethod
    def post():
        """
        Registers a new reservation given its type
        :return: JSON object with the created reservation
        """
        try:
            data = PARSER.parse_args()
            return ReservationModel.add(data).json(date_to_string=True), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    @Utils.login_required
    def put():
        """
        Updates the current reservation given its new type
        :return: JSON object with the updated reservation
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return ReservationModel.update(reservation, data.get('type')).json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    @Utils.login_required
    def get():
        """
        Retrieves the information of the current reservation
        :return:
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return reservation.calculate_price().json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401


class ReservationWithPromo(Resource):
    @staticmethod
    @Utils.login_required
    def put():
        """
        Updates the current reservation given a promo_id
        :return: JSON object with the updated prices
        """
        try:
            data = PROMO.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return reservation.insert_promo(data).json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
