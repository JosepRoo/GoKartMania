from flask import session
from flask_restful import Resource

from app import Response
from app.models.locations.errors import LocationErrors
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.locations.constants import PARSER
from app.models.users.errors import UserErrors
from app.models.locations.location import Location as LocationModel
from app.models.reservations.reservation import Reservation as ReservationModel


class Locations(Resource):
    @staticmethod
    def post():
        """
        Inserts a new location to the Locations collection
        :return: :class:`app.models.locations.location`
        """
        try:
            data = PARSER.parse_args()
            return LocationModel.add(data).json(), 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    def get(location_id=None):
        """
        Retrieves the information of all the locations in the Locations collection
        :return: JSON object with all the locations
        """
        try:
            return [location.json() for location in LocationModel.get_locations(location_id)], 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    def put():
        """
        Updates the location with the given parameters
        :return: JSON object with the updated location
        """
        try:
            data = PARSER.parse_args()
            return LocationModel.update(data).json(), 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401