from app.models.baseModel import BaseModel
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation

"""
This is the pilot model object which holds the information of the pilot if they have a licence.
"""


class Pilot(BaseModel):
    def __init__(self, name, last_name=None, email=None, location=None, birth_date=None, postal_code=None, nickname=None,
                 city=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.birth_date = birth_date
        self.postal_code = postal_code
        self.nickname = nickname
        self.city = city

    @classmethod
    def add(cls, reservation: Reservation, new_pilot):
        """
        Adds a new pilot to the given reservation party.
        :param reservation: Reservation object
        :param new_pilot: The new pilot to be added to the reservation
        :return: A brand new pilot
        """
        pilot = cls(**new_pilot)
        reservation.pilots.append(pilot)
        reservation.update_mongo(COLLECTION_TEMP)
        return pilot

    @staticmethod
    def get(reservation: Reservation, pilot_id):
        """
        Retrieves the information of the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: The requested pilot
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                return pilot
        raise PilotNotFound("El piloto con el ID dado no existe")

    @classmethod
    def update(cls, reservation: Reservation, updated_pilot, pilot_id):
        """
        Updates the information from the pilot with the given id.
        :param reservation: Reservation object containing the array of pilots
        :param updated_pilot: The pilot data to be updated to the previous one
        :param pilot_id: the ID of the pilot to be updated
        :return: All the pilots of the current reservation, with updated data
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                new_pilot = cls(**updated_pilot, _id=pilot_id)
                reservation.pilots.remove(pilot)
                reservation.pilots.append(new_pilot)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.pilots
        raise PilotNotFound("El piloto con el ID dado no existe")

    @staticmethod
    def delete(reservation: Reservation, pilot_id):
        """
        Removes from the reservations array of pilots the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: The remaining pilots of the reservation
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                reservation.pilots.remove(pilot)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.pilots
        raise PilotNotFound("El piloto con el ID dado no existe")


class AbstractPilot(BaseModel):
    from app.models.turns.turn import AbstractTurn

    def __init__(self, position, allocation_date, _id=None):
        super().__init__(_id)
        self.position = position
        self.allocation_date = allocation_date

    @classmethod
    def add(cls, turn: AbstractTurn, new_pilot):
        """
        Adds a new pilot to the given abstract turn party
        :param turn: Abstract turn object
        :param new_pilot: The new pilot to be added to the turn
        :return: Pilot object
        """
        pilot = cls(**new_pilot)
        turn.pilots.append(pilot)
        return pilot
