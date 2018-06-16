from flask import session

from app.models.baseModel import BaseModel
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation
from app.models.turns.turn import Turn


class Pilot(BaseModel):
    def __init__(self, name, last_name=None, location=None, birth_date=None, postal_code=None, nickname=None,
                 city=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.last_name = last_name
        self.location = location
        self.birth_date = birth_date
        self.postal_code = postal_code
        self.nickname = nickname
        self.city = city

    @classmethod
    def add(cls, turn: Turn, reservation: Reservation, new_pilot):
        pilot = cls(**new_pilot)
        turn.pilots.append(pilot)
        reservation.update_mongo(COLLECTION_TEMP)
        return new_pilot

    @staticmethod
    def get(reservation: Reservation, pilot_id):
        """
        Retrieves the information of the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: The requested pilot
        """
        for pilot in reservation.turns[0].pilots:
            if pilot.json()["_id"] == pilot_id:
                return pilot
        raise PilotNotFound("El piloto con el ID dado no existe")

    @classmethod
    def update(cls, reservation: Reservation, updated_pilot, pilot_id):
        """

        :param reservation:
        :param updated_pilot:
        :param pilot_id:
        :return:
        """
        for pilot in reservation.turns[0].pilots:
            if pilot.json()["_id"] == pilot_id:
                new_pilot = cls(**updated_pilot, _id=pilot_id)
                # Actualizar este piloto en todos los turnos
                for turn in reservation.turns:
                    turn.pilots[turn.pilots.index(pilot)] = new_pilot
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.turns[0].pilots
        raise PilotNotFound("El piloto con el ID dado no existe")

    @staticmethod
    def delete(reservation: Reservation, pilot_id):
        """
        Removes from the reservations array of pilots the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: The remaining pilots of the reservation
        """
        for pilot in reservation.turns[0].pilots:
            if pilot.json()["_id"] == pilot_id:
                # Quitar este piloto de todos los turnos
                for turn in reservation.turns:
                    turn.pilots.remove(pilot)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.turns[0].pilots
        raise PilotNotFound("El piloto con el ID dado no existe")
