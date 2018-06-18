from flask import session

from app.models.baseModel import BaseModel
from app.common.database import Database
from app.models.users.constants import COLLECTION as USERS_COLLECTION
from app.models.reservations.constants import COLLECTION_TEMP as RESERVATION_COLLECTION
from app.models.users.errors import InvalidEmail, UserAlreadyRegisteredError
from app.models.users.user import User
from app.models.reservations.errors import ReservationNotFound


class Reservation(BaseModel):
    def __init__(self, user_id, type, user_email, id_location, turns=list(), pilots=list(), _id=None):
        from app.models.turns.turn import Turn
        from app.models.pilots.pilot import Pilot
        super().__init__(_id)
        self.user_id = user_id
        self.type = type
        self.user_email = user_email
        self.id_location = id_location
        self.turns = [Turn(**turn) for turn in turns] if turns else turns
        self.pilots = [Pilot(**pilot) for pilot in pilots] if pilots else pilots

    @classmethod
    def add(cls, user: User, new_reservation):
        from app.models.turns.turn import Turn as TurnModel
        from app.models.pilots.pilot import Pilot as PilotModel
        reservation = cls(**new_reservation)
        reservation.save_to_mongo(RESERVATION_COLLECTION)
        # Por default, una reservación debe llevar al menos un turno y al menos un piloto
        TurnModel.add(reservation, {"schedules": "HH:MM", "turn_number": 0, "positions": {}})
        PilotModel.add(reservation, {'name': 'Piloto 1'})
        user.reservations.append(reservation._id)
        user.update_mongo(USERS_COLLECTION)
        session['reservation'] = reservation._id
        return new_reservation

    @classmethod
    def get_by_id(cls, _id, collection):
        """
        Returns the reservation object with the given id, or raises an exception if that reservation was not found
        :param _id: id of the reservation to find
        :param collection: DB that contains all the reservations
        :return: reservation object
        """
        reservation = Database.find_one(collection, {'_id': _id})
        if reservation:
            return cls(**reservation)
        raise ReservationNotFound("La reservación con el ID dado no existe.")
