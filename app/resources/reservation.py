from flask_restful import Resource

from app import Response
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.reservations.constants import PARSER
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
            user_id = data.get("user_id")
            user = UserModel.get_by_id(user_id, COLLECTION)
            return ReservationModel.add(user, data), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
