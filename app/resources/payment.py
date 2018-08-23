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

        .. :quickref: Pagos; Procesa el pago de la reservación

        **Example request**:

        .. sourcecode:: http

            POST /user/payments/<string:user_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "number": "4111111111111111",
                "name": "Aldo Arturo Reyna",
                "month": "04",
                "year": "2021",
                "cvv": "123",
                "payment_method": "MASTERCARD",
                "payment_type": "Etomin",
                "promo_id": null,
                "coupon_id": null
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Correos de confirmacion exitosamente enviados."
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "El numero de la tarjeta es invalido."
            }

        :resheader Content-Type: application/json
        :status 200: payment completed
        :status 401: malformed
        :status 500: internal error

        :return: :class:`app.models.payments.payment.Payment`
        """
        try:
            card_data, payment_data = {}, PAYMENT_PARSER.parse_args()
            if payment_data.get('payment_type') == 'Etomin':
                card_data = CARD_PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            user = UserModel.get_by_id(user_id, USER_COLLECTION)
            PaymentModel.add(user, reservation, card_data, payment_data).json()
            qr_code = QRModel.create(reservation)
            UserModel.send_confirmation_message(user, reservation, qr_code)
            PilotModel.send_confirmation_message(reservation, qr_code)
            LocationModel.admins_send_reservation_info(user, reservation, qr_code)
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
        except Exception as e:
            return Response.generic_response(e), 500
