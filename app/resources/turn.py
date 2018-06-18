from flask_restful import Resource

from app import Response
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.turns.constants import PARSER
from app.models.turns.errors import TurnErrors
from app.models.turns.turn import Turn as TurnModel


class Turns(Resource):
    @staticmethod
    def post():
        """
        Registers a new turn with the given schedules
        :return:
        """
        try:
            data = PARSER.parse_args()
            user_id = data.get("user_id")
            user = UserModel.get_by_id(user_id, COLLECTION)
            return TurnModel.add(user, data), 200
        except TurnErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
