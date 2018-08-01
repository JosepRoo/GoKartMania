from flask import session
from flask_restful import Resource

from app import Response
from app.common.utils import Utils
from app.models.dates.errors import DateErrors
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.reservations.errors import ReservationErrors
from app.models.schedules.errors import ScheduleErrors
from app.models.users.errors import UserErrors
from app.models.turns.constants import PARSER
from app.models.turns.errors import TurnErrors, TurnNotFound
from app.models.turns.turn import Turn as TurnModel
from app.models.reservations.reservation import Reservation as ReservationModel


class Turns(Resource):
    @staticmethod
    @Utils.login_required
    def post():
        """
        Registers a new turn with the given parameters (date, schedule, and turn)
        :return:
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return TurnModel.check_and_add(reservation, data).json(), 200
        except TurnErrors as e:
            return Response(message=e.message).json(), 409
        except ScheduleErrors as e:
            return Response(message=e.message).json(), 409
        except UserErrors as e:
            return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class Turn(Resource):
    @staticmethod
    @Utils.login_required
    def get(turn_id):
        """
        Retrieves the information of the turn with the given id in the parameters.
        :param turn_id: The id of the turn to be read from the reservation
        :return:
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return TurnModel.get(reservation, turn_id).json(), 200
        except TurnNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def put(turn_id, reservation_id=None):
        """
        Updates the information of the turn with the given parameters
        :param reservation_id: The id of the reservation where the turn is taken
        :param turn_id: The id of the pilot to be read from the reservation
        :return: JSON object with all the turns, with updated data
        """
        try:
            data = PARSER.parse_args()
            if reservation_id is None:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            else:
                reservation = ReservationModel.get_by_id(reservation_id, COLLECTION)
            return [turn.json() for turn in TurnModel.check_and_update(reservation, data, turn_id)], 200
        except TurnNotFound as e:
            return Response(message=e.message).json(), 404
        except ScheduleErrors as e:
            return Response(message=e.message).json(), 409
        except DateErrors as e:
            return Response(message=e.message).json(), 409
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        # except Exception as e:
        #     return Response.generic_response(e), 500
