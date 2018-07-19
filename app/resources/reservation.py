from flask import session
from flask_restful import Resource

from app import Response
from app.models.promos.errors import PromotionErrors
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.reservations.constants import PARSER, COLLECTION_TEMP, PROMO, COLLECTION as REAL_RESERVATIONS
from app.models.reservations.errors import ReservationErrors, ReservationNotFound
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
        except Exception as e:
            return Response.generic_response(e), 500

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
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def delete(reservation_id):
        """
        Deletes the reservation with the given id in the parameters.
        :param reservation_id: The id of the reservation to be deleted from the Collection
        :return: JSON object with the remaining reservation
        """
        try:
            ReservationModel.delete(reservation_id)
            return Response(success=True, message="Reservación exitosamente eliminada.").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
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
        except ReservationNotFound:
            try:
                reservation = ReservationModel.get_by_id(session['reservation'], REAL_RESERVATIONS)
                return reservation.json(), 200
            except ReservationErrors as e:
                return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

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
            return reservation.insert_promo(data.get('promo_id')).json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
