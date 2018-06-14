from app.models.baseModel import BaseModel
from app.models.pilots.errors import InvalidLogin
from app.models.reservations.constants import COLLECTION
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
        reservation.update_mongo(COLLECTION)
        return new_pilot

    @classmethod
    def update(cls, reservation: Reservation, updated_pilot):
        pilot = cls(**updated_pilot)
        reservation.turns[-1].pilots[-1] = pilot
        reservation.update_mongo(COLLECTION)
        return reservation.turns[-1].pilots
