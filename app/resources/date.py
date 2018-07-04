from flask_restful import Resource
from flask import session

from app import Response
from app.models.dates.constants import PARSER
from app.models.dates.date import Date as DateModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
import calendar


class Dates(Resource):
    @staticmethod
    def get(start_date, end_date):
        """
        Retrieves all date objects in the given range
        :param start_date: The start date in range
        :param end_date: The end date in range
        :return: JSON object with the dates in the given range
        """
        try:
            return [date.json() for date in DateModel.get_dates_in_range(start_date, end_date)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    def post():
        """
        Inserts date objects to the collection in the month and year given in the parameters
        :return: Successful response if the insertion was completed
        """
        try:
            data = PARSER.parse_args()
            month_dates = calendar.monthrange(data.get('year'), data.get('month'))[1]
            for i in range(1):
                DateModel.add(data, i+1)
            return Response(success=True, message="Registro del mes exitoso").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    def put(start_date, end_date):
        """
        Randomly auto-fills the dates in the parameters with turns and pilots
        :param start_date: The start date in range
        :param end_date: The end date in range
        :return: Successful response if the update was completed
        """
        try:
            DateModel.auto_fill(start_date, end_date)
            return Response(success=True, message="Actualización del mes exitosa").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401


class AvailableDates(Resource):
    @staticmethod
    def get(start_date, end_date):
        """
        Retrieves the dates with their status of availability in a given range
        :param start_date: The start date in range
        :param end_date: The end date in range
        :return: JSON object with the available dates in the given range
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return DateModel.get_available_dates(reservation, start_date, end_date), 200
            return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401


class AvailableSchedules(Resource):
    @staticmethod
    def get(date):
        """
        Retrieves the schedules with their status of availability in a given date
        :param date: The date to be processed
        :return: JSON object with the available schedules in the given range
        """
        try:
            if session.get('reservation'):
                reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
                return DateModel.get_available_schedules(reservation, date), 200
            return Response(message="Uso de variable de sesión no autorizada.").json(), 401
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
