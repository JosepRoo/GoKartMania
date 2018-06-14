from app.models.baseModel import BaseModel
from app.models.users.constants import COLLECTION as USERS_COLLECTION
from app.models.reservations.constants import COLLECTION as RESERVATION_COLLECTION
from app.models.users.errors import InvalidEmail, UserAlreadyRegisteredError
from app.models.users.user import User


class Reservation(BaseModel):
    def __init__(self, user_id, type, user_email, id_location, turns=list(), _id=None):
        from app.models.turns.turn import Turn
        super().__init__(_id)
        self.user_id = user_id
        self.type = type
        self.user_email = user_email
        self.id_location = id_location
        self.turns = [Turn(**turn) for turn in turns] if turns else turns

    @classmethod
    def add(cls, user: User, new_reservation):
        from app.models.turns.turn import Turn as TurnModel
        reservation = cls(**new_reservation)
        reservation.save_to_mongo(RESERVATION_COLLECTION)
        # Por default, una reservación debe llebar al menos un turno con al menos un piloto
        TurnModel.add(reservation, {"schedule": "11:00", "turn_number": 1, "reservation_id": reservation._id})
        user.reservations.append(reservation)
        user.update_mongo(USERS_COLLECTION)
        print(reservation.turns)
        return new_reservation
