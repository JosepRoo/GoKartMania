from flask_restful import Resource, reqparse
from flask import session

from app import Response
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.pilots.constants import PARSER
from app.models.pilots.pilot import Pilot as PilotModel
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel


class Pilots(Resource):
    @staticmethod
    def get():
        """
        Retrieves the information of all the pilots in the given reservation
        :return: JSON object with all the pilots
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return [pilot.json() for pilot in reservation.pilots], 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def post():
        """
        Adds a new pilot to the party
        :return: JSON object with the pilot info by default (its name)
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                pilot_number = len(reservation.pilots)
                if pilot_number >= 8:
                    return Response(message="La reservación ya no puede aceptar más pilotos.").json(), 403
                return PilotModel.add(reservation, {'name': f'Piloto {pilot_number + 1}'}), 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400


class Pilot(Resource):
    @staticmethod
    def get(pilot_id):
        """
        Retrieves the information of the pilot with the given id in the parameters.
        :param pilot_id: The id of the pilot to be read from the reservation
        :return:
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return PilotModel.get(reservation, pilot_id).json(), 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def put(pilot_id):
        """
        Updates the information of the pilot with the given parameters
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: JSON object with all the pilots, with updated data
        """
        try:
            if session.get('reservation'):
                data = PARSER.parse_args()
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return [pilot.json() for pilot in PilotModel.update(reservation, data, pilot_id)], 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def delete(pilot_id):
        """
        Deletes the pilot with the given id in the parameters.
        :param pilot_id: The id of the pilot to be deleted from the reservation
        :return: JSON object with the remaining pilots
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return [pilot.json() for pilot in PilotModel.delete(reservation, pilot_id)], 200
            return Response(message="Uso de variable de sesión no autorizada."), 401
        except PilotNotFound as e:
            return Response(message=e.message).json(), 404
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400
