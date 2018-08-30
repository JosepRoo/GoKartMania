import flask_restful
from flask import session
from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.dates.errors import DateErrors
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.reservations.errors import ReservationErrors, ReservationNotFound
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


class RetrieveTurn(Resource):
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


class AdminChangeTurn(Resource):
    @staticmethod
    @Utils.admin_login_required
    def put(reservation_id):
        """
        Updates the information of the turn with the given parameters

        :param reservation_id: The id of the reservation where the turn is taken

        .. :quickref: Turno; Cambia el turno a otra fecha, horario, turno

        **Example request**:

        .. sourcecode:: http

            PUT /user/turn/<string:reservation_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "turns": [
                    {
                        "date": "2018-08-31",
                        "schedule": "15",
                        "turn_number": "1",
                        "positions": {
                            "pos2": "lmgs.0610@gmail.com",
                            "pos3": "psanchez@sitsolutions.org"
                        }
                    },
                    {
                        "date": "2018-08-31",
                        "schedule": "15",
                        "turn_number": "3",
                        "positions": {
                            "pos2": "lmgs.0610@gmail.com",
                            "pos3": "psanchez@sitsolutions.org"
                        }
                    }
                ]
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
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
                    "turn_number": "3",
                    "positions": {
                        "pos2": "lmgs.0610@gmail.com",
                        "pos3": "psanchez@sitsolutions.org"
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
        parser = reqparse.RequestParser()
        parser.add_argument('turns',
                            type=dict,
                            required=True,
                            help="Este campo no puede ser dejado en blanco.",
                            action='append'
                            )
        turns = parser.parse_args()

        try:
            for turn in turns.get('turns'):
                # for item in list(turn.keys()):
                #     if item not in [a.name for a in PARSER.args]:
                #         del turn[item]
                for argument in [a.name for a in PARSER.args if a.required]:
                    if argument not in turn.keys():
                        msg = {argument: "Este campo no puede ser dejado en blanco."}
                        flask_restful.abort(400, message=msg)
            reservation = ReservationModel.get_by_id(reservation_id, COLLECTION)
            reservation_turns = [TurnModel.check_and_update(reservation, turns.get('turns')[i], False).json()
                                 for i in range(len(turns.get('turns')))]
            return reservation_turns, 200
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


class UserChangeTurn(Resource):
    @staticmethod
    @Utils.login_required
    def put(turn_id):
        """
        Updates the information of the turn with the given parameters

        :param turn_id: The id of the turn to be updates

        .. :quickref: Turno; Cambia el turno a otro horario, turno o posiciones

        **Example request**:

        .. sourcecode:: http

            PUT /user/alter_turn/<string:turn_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "date": "2018-08-30",
                "schedule": "11",
                "turn_number": "2",
                "positions": {
                    "pos1": "areyna@sitsolutions.org",
                    "pos2": "lmgs.0610@gmail.com"
                }
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "cffcb6231d5441c0ab689c0dc91f463c",
                "schedule": "11",
                "turn_number": "2",
                "positions": {
                    "pos1": "areyna@sitsolutions.org",
                    "pos2": "lmgs.0610@gmail.com"
                }
            }

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

        :return: :class:`app.models.turns.turn.Turn`
        """
        try:
            data = PARSER.parse_args()
            data['_id'] = turn_id
            try:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            except ReservationNotFound:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION)
            return TurnModel.check_and_update(reservation, data, True).json(), 200
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

    @staticmethod
    @Utils.login_required
    def delete(turn_id, date):
        """
        Deletes one specific turn from the current reservation

        :param date: Date from the current reservation for the turns to be deleted
        :param turn_id: The id of the turn to be updates

        .. :quickref: Turno; Cambia el turno a otro horario, turno o posiciones

        **Example request**:

        .. sourcecode:: http

            DELETE /user/alter_turn/<string:turn_id>/<string:date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Turno exitosamente eliminado."
            }

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

        :return: Success message
        """
        try:
            try:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                is_user = True
            except ReservationNotFound:
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION)
                is_user = False
            TurnModel.delete(reservation, turn_id, date, is_user)
            return Response(success=True, message="Turno exitosamente eliminado.").json(), 200
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
