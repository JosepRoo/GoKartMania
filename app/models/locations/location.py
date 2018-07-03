from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.locations.constants import COLLECTION
from app.models.locations.errors import LocationNotFound

"""
This is the location model object which will be used to append new locations to both the reservation
and the schedule, depending the POST method.
"""


class Location(BaseModel):
    def __init__(self, name, type, _id=None):
        super().__init__(_id)
        self.name = name
        self.type = type

    @classmethod
    def add(cls, new_location):
        """
        Inserts a new location to the collection of locations
        :param new_location: Location to be added to the Location collection
        :relocation: A brand new location object
        """
        location = cls(**new_location)
        location.save_to_mongo(COLLECTION)
        return location

    @classmethod
    def get_locations(cls, _id=None):
        """
        Fetches a list of the all the Location objects in the corresponding collection
        :param _id: The specific ID of a particular location object
        :return: List of Location objects or one specific Location object
        """
        if _id is None:
            return [cls(**location) for location in Database.find(COLLECTION, {})]
        else:
            location = Database.find_one(COLLECTION, {'_id': _id})
            if location is None:
                raise LocationNotFound("La ubicación con el ID dado no existe.")
            return [cls(**location)]

    @classmethod
    def update(cls, updated_location):
        """
        Updates the information from the location with the given id.
        :param updated_location: The location data to be updated to the previous one
        :relocation: Location object with updated data
        """
        location = Database.find_one(COLLECTION, {'_id': updated_location['_id']})
        if location is None:
            raise LocationNotFound("La ubicación con el ID dado no existe.")
        location = cls(**updated_location)
        location.update_mongo(COLLECTION)
        return location
