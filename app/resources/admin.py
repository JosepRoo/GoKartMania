from flask import session
from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.admins.admin import Admin as AdminModel
from app.models.emails.errors import EmailErrors
from app.models.payments.constants import PAYMENT_PARSER, CARD_PARSER
from app.models.payments.errors import PaymentErrors
from app.models.promos.errors import PromotionErrors
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.payments.payment import Payment as PaymentModel
from app.models.qrs.qr import QR as QRModel
from app.models.pilots.pilot import Pilot as PilotModel
from app.models.locations.location import Location as LocationModel
from app.models.users.constants import COLLECTION as USER_COLLECTION


class Admin(Resource):
    @staticmethod
    def post():
        """
        Registers a new admin manually given its body parameters
        :return: A brand new admin, or a session to the currently existing admin
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        data = parser.parse_args()
        try:
            return AdminModel.admin_login(data).json(), 200
        except AdminErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500


class WhoReserved(Resource):
    @staticmethod
    @Utils.login_required
    def get(date, schedule, turn):
        """
        Finds the pilots that reserved in the given date, schedule, and turn
        :param date: Date string in YYYY-MM-DD format
        :param schedule: Schedule string in HH (24) format
        :param turn: Turn if the given schedule
        :return: Pilots array
        """
        try:
            return [pilot.json() for pilot in AdminModel.who_reserved(date, schedule, turn)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500


class PartyAvgSize(Resource):
    @staticmethod
    @Utils.login_required
    def get():
        """
        Calculates the average of all races of all times
        :return: Party average
        """
        try:
            return AdminModel.get_party_avg_size(), 200
        except Exception as e:
            return Response(message=e).json(), 500


class BusyHours(Resource):
    @staticmethod
    @Utils.login_required
    def get():
        """
        Calculates the hour's business per weekday
        :return: Array containing Weekday - Schedule - Pilots
        """
        try:
            return AdminModel.get_busy_hours(), 200
        except Exception as e:
            return Response(message=e).json(), 500


class LicensedPilots(Resource):
    @staticmethod
    @Utils.login_required
    def get():
        """
        Retrieves the pilots that have requested license
        :return: Array of pilots (name and last name)
        """
        try:
            return AdminModel.get_licensed_pilots(), 200
        except Exception as e:
            return Response(message=e).json(), 500


class ReservationIncomeQty(Resource):
    @staticmethod
    @Utils.login_required
    def get(start_date, end_date):
        """
        Calculates the total income and quantity of reservations in a given date range
        :return: Quantity and income
        """
        try:
            return AdminModel.get_reservations_income_qty(start_date, end_date), 200
        except Exception as e:
            return Response(message=e).json(), 500


class PromosDiscountQty(Resource):
    @staticmethod
    @Utils.login_required
    def get(start_date, end_date):
        """
        Calculates the total discount and quantity of promos in a given date range
        :return: Quantity and discount
        """
        try:
            return AdminModel.get_promos_discount_qty(start_date, end_date), 200
        except Exception as e:
            return Response(message=e).json(), 500


class ReservationAvgPrice(Resource):
    @staticmethod
    @Utils.login_required
    def get():
        """
        Calculates the average price of all reservations of all times
        :return: Average price
        """
        try:
            return AdminModel.get_reservation_avg_price(), 200
        except Exception as e:
            return Response(message=e).json(), 500


class AdminPayments(Resource):
    @staticmethod
    @Utils.login_required
    def post(user_id=None):
        """
        Inserts a new payment to the current reservation and sends confirmation emails
        :return: :class:`app.models.payments.Payment`
        """
        try:
            card_data, payment_data = {}, PAYMENT_PARSER.parse_args()
            if payment_data.get('payment_type') == 'Etomin':
                card_data = CARD_PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            if user_id:
                user = UserModel.get_by_id(user_id, USER_COLLECTION)
            else:
                user = None
            PaymentModel.add(user, reservation, card_data, payment_data).json()
            if user:
                qr_code = QRModel.create(reservation)
                UserModel.send_confirmation_message(user, reservation, qr_code)
                PilotModel.send_confirmation_message(reservation, qr_code)
                LocationModel.send_confirmation_message(user, reservation, qr_code)
            return Response(success=True, message="Correos de confirmacion exitosamente enviados.").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except PaymentErrors as e:
            return Response(message=e.message).json(), 401
        except EmailErrors as e:
            return Response(message=str(e.message)).json(), 401
        except UserErrors as e:
            return Response(message=e.message).json(), 401
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500
