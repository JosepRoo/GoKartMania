from flask import session
from flask_restful import Resource

from app import Response
from app.common.utils import Utils
from app.models.emails.errors import EmailErrors
from app.models.payments.constants import CARD_PARSER, PAYMENT_PARSER
from app.models.payments.errors import PaymentErrors
from app.models.promos.errors import PromotionErrors
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.reservations.errors import ReservationErrors
from app.models.users.constants import COLLECTION as USER_COLLECTION
from app.models.locations.constants import COLLECTION as LOCATION_COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.pilots.pilot import Pilot as PilotModel
from app.models.locations.location import Location as LocationModel
from app.models.payments.payment import Payment as PaymentModel
from app.models.reservations.reservation import Reservation as ReservationModel
from app.models.qrs.qr import QR as QRModel


class Payments(Resource):
    @staticmethod
    @Utils.login_required
    def post(user_id):
        """
        Inserts a new payment to the current user and sends confirmation emails
        :param user_id: ID of the user to be found
        :return: :class:`app.models.payments.Payment`
        """
        try:
            card_data, payment_data = {}, PAYMENT_PARSER.parse_args()
            if payment_data.get('payment_type') == 'Etomin':
                card_data = CARD_PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            user = UserModel.get_by_id(user_id, USER_COLLECTION)
            return PaymentModel.add(user, reservation, card_data, payment_data).json(), 200
            qr_code = QRModel.create(reservation)
            #UserModel.send_confirmation_message(user, reservation, qr_code)
            #PilotModel.send_confirmation_message(reservation, qr_code)
            #LocationModel.send_confirmation_message(user, reservation, qr_code)
            return Response(success=True, message="Correos de confirmacion exitosamente enviados.").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except PaymentErrors as e:
            return Response(message=e.message).json(), 401
        except EmailErrors as e:
            return Response(message=e.message).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
