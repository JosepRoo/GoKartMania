from app.models.baseModel import BaseModel
from app.models.users.constants import COLLECTION as USERS_COLLECTION
from app.models.reservations.constants import COLLECTION as RESERVATION_COLLECTION
from app.models.users.errors import InvalidEmail, UserAlreadyRegisteredError
from app.models.users.user import User


class Reservation(BaseModel):
    def __init__(self, user_id, type, user_email, id_location, turns=list(), _id=None):
        super().__init__(_id)
        self.user_id = user_id
        self.type = type
        self.user_email = user_email
        self.id_location = id_location
        self.turns = turns

    @classmethod
    def add(cls, user: User, new_reservation):
        reservation = cls(**new_reservation)
        reservation.save_to_mongo(RESERVATION_COLLECTION)
        user.reservations.append(reservation)
        user.update_mongo(USERS_COLLECTION)
        return new_reservation
