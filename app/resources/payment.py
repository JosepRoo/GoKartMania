from flask_restful import Resource

from app import Response
from app.models.payments.constants import PARSER
from app.models.payments.errors import PaymentErrors
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.payments.payment import Payment as PaymentModel


class Payments(Resource):
    @staticmethod
    def post():
        """
        Inserts a new payment to the current user
        :return: :class:`app.models.payments.Payment`
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return PaymentModel.add(user, data), 200
        except UserException as e:
            return Response(message=e.message).json(), 401
        except PaymentException as e:
            return Response(message=e.message).json(), 400