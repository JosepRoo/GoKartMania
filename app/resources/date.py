from flask_restful import Resource
from flask import session

from app import Response
from app.common.database import Database
from app.models.dates.constants import COLLECTION
from app.models.dates.constants import PARSER
from app.models.dates.date import Date as DateModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
import calendar


class Dates(Resource):
    @staticmethod
    def get(start_date, end_date):
        try:
            return [date.json() for date in DateModel.get_dates_in_range(start_date, end_date)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def post():
        try:
            data = PARSER.parse_args()
            month_dates = calendar.monthrange(data.get('year'), data.get('month'))[1]
            for i in range(4):
                DateModel.add(data, i+1)
            return Response(success=True, message="Registro del mes exitoso").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400

    @staticmethod
    def put():
        try:
            DateModel.auto_fill()
            return Response(success=True, message="Actualización del mes exitosa").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400


class AvailableDates(Resource):
    @staticmethod
    def get():
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return DateModel.get_available_dates(reservation), 200
            # return [date.json() for date in DateModel.get_available_dates()], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400
