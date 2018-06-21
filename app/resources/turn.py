from flask import session
from flask_restful import Resource

from app import Response
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.users.errors import UserErrors
from app.models.turns.constants import PARSER
from app.models.turns.errors import TurnErrors
from app.models.turns.turn import Turn as TurnModel
from app.models.reservations.reservation import Reservation as ReservationModel


class Turns(Resource):
    @staticmethod
    def post():
        """
        Registers a new turn with the given parameters (date, schedule, and turn)
        :return:
        """
        try:
            if session.get('reservation'):
                data = PARSER.parse_args()
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                TurnModel.check_and_add(reservation, data)
                return Response(success=True, message="Registro del turno exitoso").json(), 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except TurnErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
