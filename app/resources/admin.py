from flask import session
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.admins.admin import Admin as AdminModel
from app.models.emails.errors import EmailErrors
from app.models.payments.constants import PAYMENT_PARSER, CARD_PARSER
from app.models.payments.errors import PaymentErrors
from app.models.promos.errors import PromotionErrors
from app.models.recoveries.errors import RecoveryErrors
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

        .. :quickref: Admin; Inicia la sesión del admin

        **Example request**:

        .. sourcecode:: http

            POST /admin HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "name": "Leslie",
                "email": "lgallegos@gokartmania.com",
                "password": "gokartmania2018"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "7967d9fc21644f8e8d3c7cfe0f09404d",
                "email": "lgallegos@gokartmania.com",
                "name": "Leslie"
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Credenciales incorrectas"
            }

        :resheader Content-Type: application/json
        :status 200: admin logged in
        :status 401: malformed
        :status 500: internal error

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
            return Response.generic_response(e), 500


class WhoReserved(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(date, schedule, turn):
        """
        Finds the pilots that reserved in the given date, schedule, and turn

        :param date: Date string in YYYY-MM-DD format
        :param schedule: Schedule string in HH (24) format
        :param turn: Turn if the given schedule

        .. :quickref: Pilotos; Info de los pilotos en la fecha, horario y turno elegidos

        **Example request**:

        .. sourcecode:: http

            GET /admin/who_reserved/<string: date>/<string: schedule>/<string: turn> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": "psanchez@sitsolutions.org",
                    "position": 1,
                    "allocation_date": "2018-08-01 00:26"
                },
                {
                    "_id": "lmgs.0610@gmail.com",
                    "position": 2,
                    "allocation_date": "2018-08-01 00:26"
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: pilots info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Pilots array
        """
        try:
            return [pilot.json() for pilot in AdminModel.who_reserved(date, schedule, turn)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class PartyAvgSize(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get():
        """
        Calculates the average of all races of all times

        .. :quickref: Promedio-Partida; Tamaño promedio de las carreras

        **Example request**:

        .. sourcecode:: http

            GET /admin/party_avg_size HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "11"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "12"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "14"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "15"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "16"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "19"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "20"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 1,
                        "schedule": "21"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "11"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "12"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "14"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "15"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "16"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "19"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "20"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 2,
                        "schedule": "21"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "11"
                    },
                    "party_size": 5
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "12"
                    },
                    "party_size": 3
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "13"
                    },
                    "party_size": 5
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "14"
                    },
                    "party_size": 5
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "15"
                    },
                    "party_size": 7
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "16"
                    },
                    "party_size": 5
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "19"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "20"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 3,
                        "schedule": "21"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "11"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "12"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "14"
                    },
                    "party_size": 8
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "15"
                    },
                    "party_size": 14
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "16"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "17"
                    },
                    "party_size": 3
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "19"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "20"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 4,
                        "schedule": "21"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "11"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "12"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "14"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "15"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "16"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "19"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "20"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 5,
                        "schedule": "21"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "11"
                    },
                    "party_size": 3
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "12"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "14"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "15"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "16"
                    },
                    "party_size": 8
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "19"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "20"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 6,
                        "schedule": "21"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "11"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "12"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "13"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "14"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "15"
                    },
                    "party_size": 1
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "16"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "17"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "19"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "20"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "weekday": 7,
                        "schedule": "21"
                    },
                    "party_size": 0
                }
            ]
        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: party average size retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Party average
        """
        try:
            return AdminModel.get_party_avg_size(), 200
        except Exception as e:
            return Response.generic_response(e), 500


class BusyHours(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get():
        """
        Calculates the hour's business per weekday

        .. :quickref: Ocupación-Horarios; Horarios más concurridos

        **Example request**:

        .. sourcecode:: http

            GET /admin/busy_hours HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": {
                        "schedule": "11"
                    },
                    "party_size": 12
                },
                {
                    "_id": {
                        "schedule": "12"
                    },
                    "party_size": 6
                },
                {
                    "_id": {
                        "schedule": "13"
                    },
                    "party_size": 5
                },
                {
                    "_id": {
                        "schedule": "14"
                    },
                    "party_size": 14
                },
                {
                    "_id": {
                        "schedule": "15"
                    },
                    "party_size": 22
                },
                {
                    "_id": {
                        "schedule": "16"
                    },
                    "party_size": 15
                },
                {
                    "_id": {
                        "schedule": "17"
                    },
                    "party_size": 3
                },
                {
                    "_id": {
                        "schedule": "18"
                    },
                    "party_size": 0
                },
                {
                    "_id": {
                        "schedule": "19"
                    },
                    "party_size": 3
                },
                {
                    "_id": {
                        "schedule": "20"
                    },
                    "party_size": 2
                },
                {
                    "_id": {
                        "schedule": "21"
                    },
                    "party_size": 5
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: busy hours retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Array containing Weekday - Schedule - Pilots
        """
        try:
            return AdminModel.get_busy_hours(), 200
        except Exception as e:
            return Response.generic_response(e), 500


class LicensedPilots(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get():
        """
        Retrieves the pilots that have requested license

        .. :quickref: Pilotos-Licencia; Info de los pilotos que han comprado licencia

        **Example request**:

        .. sourcecode:: http

            GET /admin/licensed_pilots HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": {
                        "name": "Josep,
                        "last_name": "Romagosa"
                    }
                },
                {
                    "_id": {
                        "name": "Aldo Arturo",
                        "last_name": "Reyna Gómez"
                    }
                }
                {
                    "_id": {
                        "name": "Michel",
                        "last_name": "Martínez Guzmán"
                    }
                },
                {
                    "_id": {
                        "name": "Leslie",
                        "last_name": "Gallegos Salazar"
                    }
                },
                {
                    "_id": {
                        "name": "Pablo Alejandro",
                        "last_name": "Sánchez Tadeo"
                    }
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: pilots info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Array of pilots (name and last name)
        """
        try:
            return AdminModel.get_licensed_pilots(), 200
        except Exception as e:
            return Response.generic_response(e), 500


class ReservationIncomeQty(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(start_date, end_date):
        """
        Calculates the total income and quantity of reservations in a given date range

        :param: start_date: The starting date to look for reservations
        :param: end_date: The ending date to look for reservations

        .. :quickref: Ganancia-Reservación; Total ganado en reservaciones y cantidad

        **Example request**:

        .. sourcecode:: http

            GET /admin/reservation_income_qty/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": null,
                    "income": 6400,
                    "qty": 13
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: total income and quantity retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Quantity and income
        """
        try:
            return AdminModel.get_reservations_income_qty(start_date, end_date), 200
        except Exception as e:
            return Response.generic_response(e), 500


class PromosDiscountQty(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(start_date, end_date):
        """
        Calculates the total discount and quantity of promos in a given date range

        :param: start_date: The starting date to look for reservations
        :param: end_date: The ending date to look for reservations

        .. :quickref: Dinero-Promoción; Total de dinero que se va en promociones

        **Example request**:

        .. sourcecode:: http

            GET /admin/promos_income_qty/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": null,
                    "discount": 455,
                    "qty": 1
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: discount money retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Quantity and discount
        """
        try:
            return AdminModel.get_promos_discount_qty(start_date, end_date), 200
        except Exception as e:
            return Response.generic_response(e), 500


class BuildReservationsReport(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(start_date, end_date):
        """
        Builds a report containing the number of pilots, number of races,
        and the price of a reservation in a given date range.

        .. :quickref: Reporte-Reservaciones; Genera un reporte con la info de reservaciones en un rango de fechas

        **Example request**:

        .. sourcecode:: http

            GET /admin/build_reservations_report/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: report created
        :status 401: malformed
        :status 500: internal error

        :return: XLSX report
        """
        try:
            return AdminModel.build_reservations_report(start_date, end_date)
        except Exception as e:
            return Response.generic_response(e), 500


class BuildPilotsReport(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get():
        """
        Builds a report containing the information of licensed pilots, their total reservations and races.

        .. :quickref: Reporte-Reservaciones; Genera un reporte con la info de reservaciones en un rango de fechas

        **Example request**:

        .. sourcecode:: http

            GET /admin/build_pilots_report HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: report created
        :status 401: malformed
        :status 500: internal error

        :return: XLSX report
        """
        try:
            return AdminModel.build_pilots_report()
        except Exception as e:
            return Response.generic_response(e), 500


class ReservationAvgPrice(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get():
        """
        Calculates the average price of all reservations of all times

        :param: start_date: The starting date to look for reservations
        :param: end_date: The ending date to look for reservations

        .. :quickref: Dinero-Reservación; Promedio del costo de una reservación

        **Example request**:

        .. sourcecode:: http

            GET /admin/reservation_avg_price HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": null,
                    "avg_price": 492.3076923076923
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: average reservation price calculated
        :status 401: malformed
        :status 500: internal error

        :return: Average price
        """
        try:
            return AdminModel.get_reservation_avg_price(), 200
        except Exception as e:
            return Response.generic_response(e), 500


class AdminPayments(Resource):
    @staticmethod
    @Utils.admin_login_required
    def post(user_id=None):
        """
        Inserts a new payment to the current reservation and sends confirmation emails

        .. :quickref: Pagos; Procesa el pago de la reservación

        **Example request**:

        .. sourcecode:: http

            POST /admin/payments HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "payment_method": null,
                "payment_type": "Admin"
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
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: payment completed
        :status 401: malformed
        :status 500: internal error

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
            return Response.generic_response(e), 500


class ForgotPassword(Resource):
    @staticmethod
    def put():
        """
        Recovers the password of the admin by sending a recovery_id through email, using Amazon Web Services

        .. :quickref: Olvidó contraseña; Envía mensaje de recuperación

        **Example request**:

        .. sourcecode:: http

            PUT /admin/forgot_password/ HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "email": "test@test.com"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Correo de recuperación exitosamente enviado."
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 400 Bad request
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Debes proporcionar un mensaje de texto o cuerpo HTML válido."
            }

        :resheader Content-Type: application/json
        :status 200: email sent
        :status 400: malformed request

        :return: Confirmation message
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        data = parser.parse_args()
        try:
            admin = AdminModel.get_by_email(data['email'])
            if admin is None:
                return Response(success=False, message="El administrador con el correo dado no existe.").json(), 400
            AdminModel.send_recovery_message(admin)
            return Response(success=True, message="Correo de recuperación exitosamente enviado.").json(), 200
        except AdminErrors as e:
            return Response(message=e.message).json(), 400
        except EmailErrors as e:
            return Response(message=e.message).json(), 400


class ResetPassword(Resource):
    @staticmethod
    def put(recovery_id):
        """
        Resets the password of the admin by using the recovery_id in tbe parameter

        .. :quickref: Reestablece contraseña; Renueva la contraseña con aquella que el administrador proporcione

        **Example request**:

        .. sourcecode:: http

            PUT /admin/reset_password/bd40995130a04067b6d6726c11e73c5e HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "email": "test@test.com",
                "new_password": "4321"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Contraseña del administrador exitosamente actualizada."
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 400 Bad request
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "No se pudo hacer la recuperación de la contraseña."
            }

        :resheader Content-Type: application/json
        :status 200: admin updated password
        :status 400: malformed request

        :return: Confirmation message
        """
        parser = reqparse.RequestParser()
        parser.add_argument('new_password',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="Este campo no puede ser dejado en blanco."
                            )
        data = parser.parse_args()
        try:
            admin = AdminModel.get_by_email(data['email'])
            if admin is None:
                return Response(success=False, message="El administrador con el correo dado no existe.").json(), 400
            AdminModel.recover_password(recovery_id, admin.email, data.new_password)
            return Response(success=True, message="Contraseña del administrador exitosamente actualizada.").json(), 200
        except AdminErrors as e:
            return Response(message=e.message).json(), 400
        except RecoveryErrors as e:
            return Response(message=e.message).json(), 400
