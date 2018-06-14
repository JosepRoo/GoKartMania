from flask_restful import Resource

from app import Response
from app.models.reservations.constants import COLLECTION
from app.models.pilots.constants import PARSER
from app.models.pilots.pilot import Pilot as PilotModel
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel


class Pilot(Resource):
    @staticmethod
    def post(reservation_id):
        """
        Adds a new pilot to the party
        :return: JSON object with the pilot info by default (its name)
        """
        try:
            reservation = ReservationModel.get_by_id(reservation_id, COLLECTION)
            pilot_number = len(reservation.turns[-1].pilots)
            if pilot_number >= 8:
                return Response(message="La reservación ya no puede aceptar más pilotos.").json(), 403
            return PilotModel.add(reservation.turns[-1], reservation, {'name': f'Piloto {pilot_number + 1}'}), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def put(reservation_id):
        """
        Updates the information of the pilot with the given parameters
        :return: JSON object with all the pilots, with updated data
        """
        try:
            data = PARSER.parse_args()
            reservation = ReservationModel.get_by_id(reservation_id, COLLECTION)
            return [pilot.json() for pilot in PilotModel.update(reservation, data)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400
