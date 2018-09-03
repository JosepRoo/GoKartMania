from flask import session
from flask_restful import Resource

from app import Response
from app.models.locations.errors import LocationErrors
from app.models.promos.errors import PromotionErrors
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserErrors
from app.models.users.user import User as UserModel
from app.models.reservations.constants import PARSER, COLLECTION_TEMP, PROMO, COLLECTION as REAL_RESERVATIONS
from app.models.reservations.errors import ReservationErrors, ReservationNotFound
from app.models.reservations.reservation import Reservation as ReservationModel
from app.common.utils import Utils


class Reservations(Resource):
    @staticmethod
    def post():
        """
        Registers a new reservation given its type

        .. :quickref: Reservaciones; Inicia el proceso de una reservación

        **Example request**:

        .. sourcecode:: http

            POST /user HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "type": "Adultos",
                "id_location": "1"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "37ed22da4292438ab316b801f3fe4517",
                "type": "Adultos",
                "date": "2018-08-01 00:00",
                "location": {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                },
                "turns": [],
                "pilots": [],
                "payment": null,
                "amount": null,
                "license_price": null,
                "turns_price": null,
                "price_before_promo": null,
                "promo_id": null,
                "coupon_id": null,
                "discount": null
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Error en el tipo de reservacion. Solo puede ser 'Adultos' o 'Niños'."
            }

        :resheader Content-Type: application/json
        :status 200: reservation process started
        :status 401: malformed
        :status 404: location ID was not found
        :status 500: internal error

        :return: JSON object with the created reservation
        """
        try:
            data = PARSER.parse_args()
            return ReservationModel.add(data).json(date_to_string=True), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except LocationErrors as e:
            return Response(message=e.message).json(), 404
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def put():
        """
        Updates the current reservation given its new type

        .. :quickref: Reservaciones; Cambia el tipo de reservación Niños-Adultos

        **Example request**:

        .. sourcecode:: http

            PUT /user/reservations HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "type": "Niños",
                "id_location": "1"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "37ed22da4292438ab316b801f3fe4517",
                "type": "Niños",
                "date": "2018-08-01 00:00",
                "location": {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                },
                "turns": [],
                "pilots": [],
                "payment": null,
                "amount": null,
                "license_price": null,
                "turns_price": null,
                "price_before_promo": null,
                "promo_id": null,
                "coupon_id": null,
                "discount": null
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Error en el tipo de reservacion. Solo puede ser 'Adultos' o 'Niños'."
            }

        :resheader Content-Type: application/json
        :status 200: reservation type changed
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the updated reservation
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return ReservationModel.update(reservation, data.get('type')).json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def delete(reservation_id):
        """
        Deletes the reservation with the given id in the parameters.

        .. :quickref: Reservaciones; Elimina una reservación

        **Example request**:

        .. sourcecode:: http

            DELETE /user/reservations/<string:reservation_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Reservación exitosamente eliminada."
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La reservacion con el ID dado no existe."
            }

        :resheader Content-Type: application/json
        :status 200: reservation deleted
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the remaining reservation
        """
        try:
            ReservationModel.delete(reservation_id)
            return Response(success=True, message="Reservación exitosamente eliminada.").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    @Utils.turn_required
    def get():
        """
        Retrieves the information of the current reservation

        .. :quickref: Reservaciones; Info de una reservación

        **Example request**:

        .. sourcecode:: http

            GET /user/reservations HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "135327d47c8845aaa7fe1ad094ea9a7a",
                "type": "Adultos",
                "date": "2018-08-01 00:25",
                "location": {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                },
                "turns": [
                    {
                        "_id": "273d2975ee684bc39306d62ee9069bcb",
                        "schedule": "11",
                        "turn_number": "1",
                        "positions": {
                            "pos1": "psanchez@sitsolutions.org",
                            "pos2": "lmgs.0610@gmail.com"
                        }
                    }
                ],
                "pilots": [
                    {
                        "_id": "lmgs.0610@gmail.com",
                        "name": "Leslie",
                        "last_name": "Gallegos Salazar",
                        "email": "lmgs.0610@gmail.com",
                        "location": "Plaza Carso",
                        "birth_date": "22-08-96",
                        "postal_code": "50840",
                        "nickname": "Leslie",
                        "city": "Estado de México",
                        "licensed": true
                    },
                    {
                        "_id": "psanchez@sitsolutions.org",
                        "name": "Pablo Alejandro",
                        "last_name": "Sanchez Tadeo",
                        "email": "psanchez@sitsolutions.org",
                        "location": "Plaza Carso",
                        "birth_date": "17-07-96",
                        "postal_code": "50840",
                        "nickname": "Pablito",
                        "city": "Estado de México",
                        "licensed": true
                    }
                ],
                "payment": null,
                "amount": 495,
                "license_price": 200,
                "turns_price": 295,
                "price_before_promo": null,
                "promo_id": null,
                "coupon_id": null,
                "discount": null
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
        :status 200: reservation info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: :class:`app.models.reservations.reservation.Reservation`
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return reservation.calculate_price().json(), 200
        except ReservationNotFound:
            try:
                reservation = ReservationModel.get_by_id(session['reservation'], REAL_RESERVATIONS)
                return reservation.json(), 200
            except ReservationErrors as e:
                return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class RetrieveReservation(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(reservation_id):
        """
        Retrieves the reservation with the given id in the parameters.

        .. :quickref: Reservaciones; Obtiene una reservación con el ID especificado

        **Example request**:

        .. sourcecode:: http

            GET /reservation/<string:reservation_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "349294d63f414c6d8f1e2557b0821ee5",
                "type": "Adultos",
                "date": "2018-08-15 10:47",
                "location": {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                },
                "turns": [
                    {
                        "_id": "1369f9d0c9a3402daf0e47c5f517b92d",
                        "schedule": "11",
                        "turn_number": "2",
                        "positions": {
                            "pos5": "areyna@sitsolutions.org",
                            "pos6": "lmgs.0610@gmail.com"
                        }
                    }
                ],
                "pilots": [
                    {
                        "_id": "areyna@sitsolutions.org",
                        "name": "Aldo Arturo",
                        "last_name": "Reyna Gómez",
                        "email": "areyna@sitsolutions.org",
                        "location": "Plaza Carso",
                        "birth_date": "01-04-95",
                        "postal_code": "07270",
                        "nickname": "iThinkEmo",
                        "city": "CDMX",
                        "licensed": true
                    },
                    {
                        "_id": "lmgs.0610@gmail.com",
                        "name": "Leslie",
                        "last_name": "Gallegos Salazar",
                        "email": "lmgs.0610@gmail.com",
                        "location": "Plaza Carso",
                        "birth_date": "22-08-96",
                        "postal_code": "50840",
                        "nickname": "Leslie",
                        "city": "Estado de México",
                        "licensed": true
                    }
                ],
                "amount": 790,
                "license_price": 200,
                "turns_price": 590,
                "price_before_promo": null,
                "promo_id": null,
                "coupon_id": null,
                "discount": null
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La reservacion con el ID dado no existe."
            }

        :resheader Content-Type: application/json
        :status 200: reservation retrieved
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the reservation
        """
        try:
            reservation = ReservationModel.get_by_id(reservation_id, REAL_RESERVATIONS)
            return reservation.json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class ReservationsDates(Resource):
    @staticmethod
    @Utils.login_required
    def get(start_date, end_date):
        """
        Retrieves the information of the reservations in a given date range

        :param: start_date: The starting date to look for reservations
        :param: end_date: The ending date to look for reservations

        .. :quickref: Reservaciones-Fecha; Info de varias reservaciones en un rango de fechas

        **Example request**:

        .. sourcecode:: http

            GET /user/reservations/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": "3b085f91f79b41f69aaf6209473f2d17",
                    "type": "Adultos",
                    "date": "2018-07-18 18:07",
                    "location": {
                        "_id": "1",
                        "name": "Plaza Carso",
                        "type": {
                            "GOKART": [
                                295,
                                530,
                                690
                            ],
                            "CADET": [
                                295,
                                530,
                                690
                            ],
                            "LICENCIA": 100
                        }
                    },
                    "turns": [
                        {
                            "_id": "21d1102232874b06a247c37827eba888",
                            "schedule": "14",
                            "turn_number": "1",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos2": "lmgs.0610@gmail.com",
                                "pos3": "psanchez@sitsolutions.org",
                                "pos4": "a01370622@gmail.com"
                            }
                        },
                        {
                            "_id": "688deb7a22f94239901f5d0f2e770b3d",
                            "schedule": "14",
                            "turn_number": "2",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos2": "lmgs.0610@gmail.com",
                                "pos3": "psanchez@sitsolutions.org",
                                "pos4": "a01370622@gmail.com"
                            }
                        },
                        {
                            "_id": "bbcdb639647f4246b656d6255465b9c1",
                            "schedule": "14",
                            "turn_number": "3",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos2": "lmgs.0610@gmail.com",
                                "pos3": "psanchez@sitsolutions.org",
                                "pos4": "a01370622@gmail.com"
                            }
                        }
                    ],
                    "pilots": [
                        {
                            "_id": "aldo_chikai@hotmail.com",
                            "name": "Aldo Arturo",
                            "last_name": "Reyna Gómez",
                            "email": "aldo_chikai@hotmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "01-04-95",
                            "postal_code": "07270",
                            "nickname": "iThinkEmo",
                            "city": "CDMX",
                            "licensed": true
                        },
                        {
                            "_id": "a01370622@gmail.com",
                            "name": "Michel",
                            "last_name": "Martínez Guzmán",
                            "email": "a01370622@gmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "28-02-96",
                            "postal_code": "54700",
                            "nickname": "Michigan",
                            "city": "Estado de México",
                            "licensed": true
                        },
                        {
                            "_id": "lmgs.0610@gmail.com",
                            "name": "Leslie",
                            "last_name": "Gallegos Salazar",
                            "email": "lmgs.0610@gmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "22-08-96",
                            "postal_code": "50840",
                            "nickname": "Leslie",
                            "city": "Estado de México",
                            "licensed": true
                        },
                        {
                            "_id": "psanchez@sitsolutions.org",
                            "name": "Pablo Alejandro",
                            "last_name": "Sanchez Tadeo",
                            "email": "psanchez@sitsolutions.org",
                            "location": "Plaza Carso",
                            "birth_date": "17-07-96",
                            "postal_code": "50840",
                            "nickname": "Pablito",
                            "city": "Estado de México",
                            "licensed": true
                        }
                    ],
                    "amount": 1090,
                    "license_price": 400,
                    "turns_price": 690,
                    "price_before_promo": null,
                    "promo_id": null,
                    "coupon_id": null,
                    "discount": null
                },
                {
                    "_id": "786779573741465cbda42b64019e0990",
                    "type": "Adultos",
                    "date": "2018-07-18 19:35",
                    "location": {
                        "_id": "1",
                        "name": "Plaza Carso",
                        "type": {
                            "GOKART": [
                                295,
                                530,
                                690
                            ],
                            "CADET": [
                                295,
                                530,
                                690
                            ],
                            "LICENCIA": 100
                        }
                    },
                    "turns": [
                        {
                            "_id": "5eab6bc8f4fb48a8a615520cf75fe086",
                            "schedule": "15",
                            "turn_number": "1",
                            "positions": {
                                "pos2": "lmgs.0610@gmail.com",
                                "pos3": "psanchez@sitsolutions.org"
                            }
                        },
                        {
                            "_id": "96e91813a5ee49ac95161b25693083f5",
                            "schedule": "15",
                            "turn_number": "2",
                            "positions": {
                                "pos2": "lmgs.0610@gmail.com",
                                "pos3": "psanchez@sitsolutions.org"
                            }
                        }
                    ],
                    "pilots": [
                        {
                            "_id": "lmgs.0610@gmail.com",
                            "name": "Leslie",
                            "last_name": "Gallegos Salazar",
                            "email": "lmgs.0610@gmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "22-08-96",
                            "postal_code": "50840",
                            "nickname": "Leslie",
                            "city": "Estado de México",
                            "licensed": true
                        },
                        {
                            "_id": "psanchez@sitsolutions.org",
                            "name": "Pablo Alejandro",
                            "last_name": "Sanchez Tadeo",
                            "email": "psanchez@sitsolutions.org",
                            "location": "Plaza Carso",
                            "birth_date": "17-07-96",
                            "postal_code": "50840",
                            "nickname": "Pablito",
                            "city": "Estado de México",
                            "licensed": true
                        }
                    ],
                    "amount": 730,
                    "license_price": 200,
                    "turns_price": 530,
                    "price_before_promo": null,
                    "promo_id": null,
                    "coupon_id": null,
                    "discount": null
                },
                {
                    "_id": "df0f6f84b5a244cf9e81a54698d0a7dc",
                    "type": "Adultos",
                    "date": "2018-07-18 19:48",
                    "location": {
                        "_id": "1",
                        "name": "Plaza Carso",
                        "type": {
                            "GOKART": [
                                295,
                                530,
                                690
                            ],
                            "CADET": [
                                295,
                                530,
                                690
                            ],
                            "LICENCIA": 100
                        }
                    },
                    "turns": [
                        {
                            "_id": "675be8fbaf4b41658b8ccf224bf73a8f",
                            "schedule": "15",
                            "turn_number": "2",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos4": "a01370622@gmail.com"
                            }
                        },
                        {
                            "_id": "7d90eb3493264cbb9e471575be18aedf",
                            "schedule": "15",
                            "turn_number": "1",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos4": "a01370622@gmail.com"
                            }
                        },
                        {
                            "_id": "fb397a0bf3934348879248fd6acaa0d4",
                            "schedule": "15",
                            "turn_number": "3",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos4": "a01370622@gmail.com"
                            }
                        },
                        {
                            "_id": "ba219e4a5d824daa976a1a52e89a0eac",
                            "schedule": "15",
                            "turn_number": "4",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos4": "a01370622@gmail.com"
                            }
                        }
                    ],
                    "pilots": [
                        {
                            "_id": "aldo_chikai@hotmail.com",
                            "name": "Aldo Arturo",
                            "last_name": "Reyna Gómez",
                            "email": "aldo_chikai@hotmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "01-04-95",
                            "postal_code": "07270",
                            "nickname": "iThinkEmo",
                            "city": "CDMX",
                            "licensed": true
                        },
                        {
                            "_id": "a01370622@gmail.com",
                            "name": "Michel",
                            "last_name": "Martínez Guzmán",
                            "email": "a01370622@gmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "28-02-96",
                            "postal_code": "54700",
                            "nickname": "Michigan",
                            "city": "Estado de México",
                            "licensed": true
                        }
                    ],
                    "amount": 730,
                    "license_price": 200,
                    "turns_price": 530,
                    "price_before_promo": 1185,
                    "promo_id": "554b84b6936f48f2b02192412e78ce10",
                    "coupon_id": "carr-d077d",
                    "discount": 455
                },
                {
                    "_id": "7d4e7a1f3bcc46f9af61f686ef60f146",
                    "type": "Adultos",
                    "date": "2018-07-20 00:00",
                    "location": {
                        "_id": "1",
                        "name": "Plaza Carso",
                        "type": {
                            "GOKART": [
                                295,
                                530,
                                690
                            ],
                            "CADET": [
                                295,
                                530,
                                690
                            ],
                            "LICENCIA": 100
                        }
                    },
                    "turns": [
                        {
                            "_id": "85118e39efdf47dc9524de8cfe49f606",
                            "schedule": "11",
                            "turn_number": "1",
                            "positions": {
                                "pos1": "aldo_chikai@hotmail.com",
                                "pos2": "lmgs.0610@gmail.com"
                            }
                        }
                    ],
                    "pilots": [
                        {
                            "_id": "aldo_chikai@hotmail.com",
                            "name": "Aldo Arturo",
                            "last_name": "Reyna Gómez",
                            "email": "aldo_chikai@hotmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "01-04-95",
                            "postal_code": "07270",
                            "nickname": "iThinkEmo",
                            "city": "CDMX",
                            "licensed": true
                        },
                        {
                            "_id": "lmgs.0610@gmail.com",
                            "name": "Leslie",
                            "last_name": "Gallegos Salazar",
                            "email": "lmgs.0610@gmail.com",
                            "location": "Plaza Carso",
                            "birth_date": "22-08-96",
                            "postal_code": "50840",
                            "nickname": "Leslie",
                            "city": "Estado de México",
                            "licensed": true
                        }
                    ],
                    "amount": 495,
                    "license_price": 200,
                    "turns_price": 295,
                    "price_before_promo": null,
                    "promo_id": null,
                    "coupon_id": null,
                    "discount": null
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
        :status 200: reservations info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Array of :class:`app.models.reservations.reservation.Reservation`
        """
        try:
            reservation = ReservationModel.get_reservations_in_time(start_date, end_date)
            return [r.json() for r in reservation], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class ReservationWithPromo(Resource):
    @staticmethod
    @Utils.login_required
    def put():
        """
        Updates the current reservation given a promo_id

        .. :quickref: Reservaciones-Promo; Actualiza los precios de la reservación con una promoción

        **Example request**:

        .. sourcecode:: http

            PUT /user/reservations_promo HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "promo_id": "desc-2de77"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "f6a96f2f5fdd4c2d829aaa602706f4f8",
                "type": "Adultos",
                "date": "2018-08-01 12:09",
                "location": {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                },
                "turns": [],
                "pilots": [],
                "payment": null,
                "amount": 448.5,
                "license_price": 0,
                "turns_price": 690,
                "price_before_promo": 690,
                "promo_id": "f2934de9ef624ad48404e97c2b941955",
                "coupon_id": "desc-2de77",
                "discount": 241.49999999999997
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La promoción con el ID dado ya expiró."
            }

        :resheader Content-Type: application/json
        :status 200: reservation prices updated
        :status 401: non-existent or expired coupon
        :status 500: internal error

        :return: JSON object with the updated prices
        """
        try:
            data = PROMO.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return reservation.insert_promo(data.get('promo_id')).json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
