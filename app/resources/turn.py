from flask import session
from flask_restful import Resource

from app import Response
from app.common.utils import Utils
from app.models.dates.errors import DateErrors
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.reservations.errors import ReservationErrors
from app.models.schedules.errors import ScheduleErrors
from app.models.users.errors import UserErrors
from app.models.turns.constants import PARSER
from app.models.turns.errors import TurnErrors, TurnNotFound
from app.models.turns.turn import Turn as TurnModel
from app.models.reservations.reservation import Reservation as ReservationModel


class Turns(Resource):
    @staticmethod
    @Utils.login_required
    def post():
        """
        Registers a new turn with the given parameters (date, schedule, and turn)

        .. :quickref: Turnos; Añade un turno a la reservación

        **Example request**:

        .. sourcecode:: http

            POST /user/turns HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "date": "2018-08-01",
                "schedule": "15",
                "turn_number": "1",
                "positions": {
                    "pos1": "psanchez@sitsolutions.org",
                    "pos2": "lmgs.0610@gmail.com"
                }
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "6d76a060d4da4acca026f10dffc960db",
                "schedule": "15",
                "turn_number": "1",
                "positions": {
                    "pos1": "psanchez@sitsolutions.org",
                    "pos2": "lmgs.0610@gmail.com"
                }
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 403 Conflict
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Este turno ya no se encuentra disponible."
            }

        :resheader Content-Type: application/json
        :status 200: turn added to reservation
        :status 401: malformed
        :status 409: turn was occupied by someone else
        :status 500: internal error

        :return: :class:`app.models.turns.turn.Turn`
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return TurnModel.check_and_add(reservation, data).json(), 200
        except TurnErrors as e:
            return Response(message=e.message).json(), 409
        except ScheduleErrors as e:
            return Response(message=e.message).json(), 409
        except UserErrors as e:
            return Response(message=e.message).json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class Turn(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(turn_id):
        """
        Retrieves the information of the turn with the given id in the parameters.

        :param turn_id: The id of the turn to be read from the reservation

        .. :quickref: Turno; Info del turno con el ID dado

        **Example request**:

        .. sourcecode:: http

            GET /user/turn/<string:turn_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "6d76a060d4da4acca026f10dffc960db",
                "schedule": "15",
                "turn_number": "1",
                "positions": {
                    "pos1": "psanchez@sitsolutions.org",
                    "pos2": "lmgs.0610@gmail.com"
                }
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
        :status 200: turn info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: :class:`app.models.turns.turn.Turn`
        """
        try:
            return TurnModel.get(turn_id), 200
        except TurnNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def put(turn_id, reservation_id=None):
        """
        Updates the information of the turn with the given parameters

        :param reservation_id: The id of the reservation where the turn is taken
        :param turn_id: The id of the pilot to be read from the reservation

        .. :quickref: Turno; Cambia el turno a otra fecha, horario, turno

        **Example request**:

        .. sourcecode:: http

            PUT /user/turn/<string:reservation_id>/<string:turn_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "date": "2018-08-31",
                "schedule": "16",
                "turn_number": "1",
                "positions": {
                    "pos1": "aldo_chikai@hotmail.com",
                    "pos2": "lmgs.0610@gmail.com",
                    "pos3": "psanchez@sitsolutions.org",
                    "pos4": "a01370622@gmail.com"
                }
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
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
                },
                {
                    "_id": "21d1102232874b06a247c37827eba888",
                    "schedule": "16",
                    "turn_number": "1",
                    "positions": {
                        "pos1": "aldo_chikai@hotmail.com",
                        "pos2": "lmgs.0610@gmail.com",
                        "pos3": "psanchez@sitsolutions.org",
                        "pos4": "a01370622@gmail.com"
                    }
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "El turno con el ID dado no existe"
            }

        :resheader Content-Type: application/json
        :status 200: turn schedule changed
        :status 401: malformed
        :status 404: turn was not found
        :status 409: turn was occupied by someone else
        :status 500: internal error

        :return: Array of :class:`app.models.turns.turn.Turn`
        """
        try:
            data = PARSER.parse_args()
            if reservation_id is None:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            else:
                reservation = ReservationModel.get_by_id(reservation_id, COLLECTION)
            return [turn.json() for turn in TurnModel.check_and_update(reservation, data, turn_id)], 200
        except TurnNotFound as e:
            return Response(message=e.message).json(), 404
        except ScheduleErrors as e:
            return Response(message=e.message).json(), 409
        except DateErrors as e:
            return Response(message=e.message).json(), 409
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
