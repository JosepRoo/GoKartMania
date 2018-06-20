from flask_restful import Resource

from app import Response
from app.common.database import Database
from app.models.dates.constants import COLLECTION
from app.models.dates.constants import PARSER
from app.models.dates.date import Date as DateModel
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
import calendar


class Dates(Resource):
    @staticmethod
    def get():
        try:
            # dates = Database.find(COLLECTION, {})
            # arr = []
            # for date in dates:
            #     arr.append(date)
            # print(arr)
            return [date.json() for date in DateModel.get_all_dates()], 200
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
            # date = DateModel(**Database.find(COLLECTION, {})[0])
            # print(date.schedules[0].turns[0].type)
            # date.schedules[0].turns[0].type = "Niño"
            # print(date.schedules[0].turns[0].type)
            DateModel.auto_fill()
            # date.update_mongo(COLLECTION)
            return Response(success=True, message="Actualización del mes exitosa").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 400
