from flask_restful import Resource, reqparse

from app import Response
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.dates.constants import PARSER
from app.models.dates.date import Date as DateModel
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
import calendar

class Dates(Resource):
    @staticmethod
    def get(reservation_id):
        """
        Retrieves the information of all the pilots in the given reservation
        :param reservation_id: The ID of the reservation to which the pilot array is to be read
        :return: JSON object with all the pilots
        """
        try:
            reservation = ReservationModel.get_by_id(reservation_id, COLLECTION_TEMP)
            return [pilot.json() for pilot in reservation.pilots], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def post():
        try:
            data = PARSER.parse_args()
            month_dates = calendar.monthrange(data.get('year'), data.get('month'))[1]
            for i in range(month_dates):
                DateModel.add(data, i+1)
            return Response(success=True, message="Registro del mes exitoso").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400
