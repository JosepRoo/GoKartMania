from app.models.baseModel import BaseModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation
from app.models.schedules.schedule import Schedule


class Turn(BaseModel):
    def __init__(self, schedule, turn_number, positions, _id=None):
        super().__init__(_id)
        self.schedule = schedule
        self.turn_number = turn_number
        self.positions = positions

    @classmethod
    def add(cls, reservation: Reservation, new_turn):
        turn = cls(**new_turn)
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION_TEMP)
        return new_turn


class AbstractTurn(BaseModel):
    def __init__(self, turn_number, type=None, pilots=list(), _id=None):
        from app.models.pilots.pilot import AbstractPilot
        super().__init__(_id)
        self.turn_number = turn_number
        self.type = type
        self.pilots = [AbstractPilot(**pilot) for pilot in pilots] if pilots else pilots

    @classmethod
    def add(cls, schedule: Schedule, new_turn):
        turn = cls(**new_turn)
        schedule.turns.append(turn)
        return turn

