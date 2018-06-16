from app.models.baseModel import BaseModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation


class Turn(BaseModel):
    def __init__(self, schedule, turn_number,  reservation_id, pilots=list(), _id=None):
        from app.models.pilots.pilot import Pilot
        super().__init__(_id)
        self.schedule = schedule
        self.turn_number = turn_number
        self.reservation_id = reservation_id
        self.pilots = [Pilot(**pilot) for pilot in pilots] if pilots else pilots

    @classmethod
    def add(cls, reservation: Reservation, new_turn):
        from app.models.pilots.pilot import Pilot as PilotModel
        turn = cls(**new_turn)
        PilotModel.add(turn, reservation, {'name': 'Piloto 1'})
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION_TEMP)
        return new_turn
