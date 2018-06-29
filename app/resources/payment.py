from flask import session
from flask_restful import Resource

from app import Response
from app.models.payments.constants import PARSER
from app.models.payments.errors import PaymentErrors
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.users.constants import COLLECTION
from app.models.schedules.errors import ScheduleErrors
from app.models.turns.errors import TurnErrors
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.payments.payment import Payment as PaymentModel
from app.models.reservations.reservation import Reservation as ReservationModel


class Payments(Resource):
    @staticmethod
    def post(user_id):
        """
        Inserts a new payment to the current user
        :param user_id: ID of the user to be found
        :return: :class:`app.models.payments.Payment`
        """
        try:
            if session.get('reservation'):
                data = PARSER.parse_args()
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                user = UserModel.get_by_id(user_id, COLLECTION)
                return PaymentModel.add(user, reservation, data), 200
            return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        except TurnErrors as e:
            return Response(message=e.message).json(), 401
        except ScheduleErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
