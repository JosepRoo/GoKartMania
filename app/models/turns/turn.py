from app.models.baseModel import BaseModel
from app.models.reservations.constants import COLLECTION
from app.models.reservations.reservation import Reservation


class Turn(BaseModel):
    def __init__(self, schedule, turn_number,  reservation_id, pilots=list(), _id=None):
        super().__init__(_id)
        self.schedule = schedule
        self.turn_number = turn_number
        self.reservation_id = reservation_id
        self.pilots = pilots

    @classmethod
    def add(cls, reservation: Reservation, new_turn):
        turn = cls(**new_turn)
        print(reservation.turns)
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION)
        return new_turn
