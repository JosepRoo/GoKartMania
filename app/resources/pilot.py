import flask_restful
from flask_restful import Resource, reqparse
from flask import session

from app import Response
from app.common.utils import Utils
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.pilots.constants import PARSER
from app.models.pilots.pilot import Pilot as PilotModel
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel


class FakeRequest(dict):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


class Pilots(Resource):
    @staticmethod
    @Utils.login_required
    def get():
        """
        Retrieves the information of all the pilots in the given reservation

        .. :quickref: Pilotos; Info de los pilotos en la reservación

        **Example request**:

        .. sourcecode:: http

            GET /user/pilots HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
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

        :return: Array of :class:`app.models.pilots.pilot.Pilot`
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return [pilot.json() for pilot in reservation.pilots], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def post():
        """
        Adds a new pilot to the party

        .. :quickref: Pilotos; Añade pilotos a la reservación

        **Example request**:

        .. sourcecode:: http

            POST /user/pilots HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "pilots": [
                    {
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
                ]
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
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
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 403 Forbidden
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La reservación ya no puede aceptar más pilotos."
            }

        :resheader Content-Type: application/json
        :status 200: pilots added to reservation
        :status 400: argument missing
        :status 401: malformed
        :status 403: number of pilots exceeded
        :status 500: internal error

        :return: Array of :class:`app.models.pilots.pilot.Pilot`
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pilots',
                            type=dict,
                            required=True,
                            help="Este campo no puede ser dejado en blanco.",
                            action='append'
                            )
        pilots = parser.parse_args()

        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            pilot_number = len(reservation.pilots)
            if pilot_number >= 8:
                return Response(message="La reservación ya no puede aceptar más pilotos.").json(), 403
            for pilot in pilots.get('pilots'):
                for item in list(pilot.keys()):
                    if item not in [a.name for a in PARSER.args]:
                        del pilot[item]
                for argument in [a.name for a in PARSER.args if a.required]:
                    if argument not in pilot.keys():
                        msg = {argument: "Este campo no puede ser dejado en blanco."}
                        flask_restful.abort(400, message=msg)
            reservation_pilots = [PilotModel.add(reservation, pilots.get('pilots')[i]).json() for i in
                                  range(len(pilots.get('pilots')))]
            ReservationModel.remove_temporal_reservations()
            return reservation_pilots
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class Pilot(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(pilot_id):
        """
        Retrieves the information of the pilot with the given id in the parameters.

        :param pilot_id: The id of the pilot to be read from the reservation

        .. :quickref: Piloto; Info del piloto con el ID dado

        **Example request**:

        .. sourcecode:: http

            GET /user/pilot/<string:pilot_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

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

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not Found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "El piloto con el ID dado no existe"
            }

        :resheader Content-Type: application/json
        :status 200: pilot info retrieved
        :status 401: malformed
        :status 404: pilot was not found
        :status 500: internal error

        :return: :class:`app.models.pilots.pilot.Pilot`
        """
        try:
            return PilotModel.get(pilot_id), 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def put(pilot_id):
        """
        Updates the information of the pilot with the given parameters

        :param pilot_id: The id of the pilot to be read from the reservation

        .. :quickref: Piloto; Cambia cierta información del piloto

        **Example request**:

        .. sourcecode:: http

            PUT /user/pilot/<string:pilot_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "name": "Michelle",
                "last_name": "Martínez Guzmán",
                "email": "a01370622@gmail.com",
                "location": "Plaza Carso",
                "birth_date": "28-02-96",
                "postal_code": "54700",
                "nickname": "Michigan",
                "city": "Estado de México",
                "licensed": true
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "a01370622@gmail.com",
                "name": "Michelle",
                "last_name": "Martínez Guzmán",
                "email": "a01370622@gmail.com",
                "location": "Plaza Carso",
                "birth_date": "28-02-96",
                "postal_code": "54700",
                "nickname": "Michigan",
                "city": "Estado de México",
                "licensed": "True"
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not Found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "El piloto con el ID dado no existe"
            }

        :resheader Content-Type: application/json
        :status 200: pilot info changed
        :status 401: malformed
        :status 404: pilot was not found
        :status 500: internal error

        :return: :class:`app.models.pilots.pilot.Pilot`
        """
        try:
            data = PARSER.parse_args()
            return PilotModel.update(data, pilot_id).json(), 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def delete(pilot_id):
        """
        Deletes the pilot with the given id in the parameters.

        :param pilot_id: The id of the pilot to be deleted from the reservation

        .. :quickref: Piloto; Elimina el piloto con el ID dado

        **Example request**:

        .. sourcecode:: http

            DELETE /user/pilot/<string:pilot_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Piloto exitosamente eliminado."
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "El piloto con el ID dado no existe"
            }

        :resheader Content-Type: application/json
        :status 200: reservation deleted
        :status 401: malformed
        :status 500: internal error

        :return: Success message
        """
        try:
            PilotModel.delete(pilot_id)
            return Response(success=True, message="Piloto exitosamente eliminado.").json(), 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
