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
        :return: JSON object with all the pilots
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return [pilot.json() for pilot in reservation.pilots], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500

    @staticmethod
    @Utils.login_required
    def post():
        """
        Adds a new pilot to the party
        :return: JSON object with the pilot info by default (its name)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pilots',
                            type=dict,
                            required=True,
                            help="Este campo no puede ser dejado en blanco.",
                            action='append'
                            )
        pilots = parser.parse_args()

        """
        nested_parser.add_argument('name',
                                    type=str,
                                    location=('pilots',),
                                    required=True,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('last_name',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('location',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('birth_date',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('postal_code',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('nickname',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('city',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        nested_parser.add_argument('name',
                                    type=str,
                                    location=('pilots',),
                                    required=False,
                                    help="Este campo no puede ser dejado en blanco."
                                    )
        pilot_data = nested_one_parser.parse_args(req=pilots)
        print(pilot_data)
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            pilot_number = len(reservation.pilots)
            if pilot_number >= 8:
                return Response(message="La reservacion ya no puede aceptar mas pilotos.").json(), 403
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
            return reservation_pilots
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500


class Pilot(Resource):
    @staticmethod
    @Utils.login_required
    def get(pilot_id):
        """
        Retrieves the information of the pilot with the given id in the parameters.
        :param pilot_id: The id of the pilot to be read from the reservation
        :return:
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return PilotModel.get(reservation, pilot_id).json(), 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500

    @staticmethod
    @Utils.login_required
    def put(pilot_id):
        """
        Updates the information of the pilot with the given parameters
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: JSON object with all the pilots, with updated data
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return [pilot.json() for pilot in PilotModel.update(reservation, data, pilot_id)], 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500

    @staticmethod
    @Utils.login_required
    def delete(pilot_id):
        """
        Deletes the pilot with the given id in the parameters.
        :param pilot_id: The id of the pilot to be deleted from the reservation
        :return: JSON object with the remaining pilots
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return [pilot.json() for pilot in PilotModel.delete(reservation, pilot_id)], 200
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response(message=e).json(), 500
