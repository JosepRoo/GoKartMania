from flask import session
import datetime
from tzlocal import get_localzone
from app.models.baseModel import BaseModel
from app.common.database import Database
from app.models.reservations.constants import COLLECTION_TEMP, TIMEOUT
from app.models.locations.constants import COLLECTION
from app.models.locations.location import Location as LocationModel
from app.models.reservations.errors import ReservationNotFound, WrongReservationType

"""
This is the reservation model object which will be used to store the temporal and real collections of the user,
when they complete the process of reservation and the payment is processed.
"""


class Reservation(BaseModel):
    def __init__(self, type, date, location=None, payment=None, turns=list(), pilots=list(), _id=None):
        from app.models.turns.turn import Turn
        from app.models.pilots.pilot import Pilot
        from app.models.payments.payment import Payment
        from app.models.locations.location import Location
        super().__init__(_id)
        self.type = type
        self.date = date
        self.location = Location(**location) if location else location
        self.turns = [Turn(**turn) for turn in turns] if turns else turns
        self.pilots = [Pilot(**pilot) for pilot in pilots] if pilots else pilots
        self.payment = Payment(**payment) if payment else payment

    @classmethod
    def add(cls, new_reservation):
        """
        Adds a new reservation to the Temporal Reservation Collection, when the user starts the process
        :param new_reservation: Reservation object with user information
        :return: Reservation object
        """
        from app.models.turns.turn import Turn as TurnModel
        from app.models.pilots.pilot import Pilot as PilotModel
        id_location = new_reservation.pop('id_location')
        location = Database.find_one(COLLECTION, {'_id': id_location})
        now = datetime.datetime.now().astimezone(get_localzone())
        reservation = cls(**new_reservation, date=now)
        print(reservation.date)
        reservation.location = LocationModel(**location)
        if reservation.type != "Niños" and reservation.type != "Adultos":
            raise WrongReservationType("Error en el tipo de reservación. Solo puede ser 'Adultos' o 'Niños'.")
        reservation.save_to_mongo(COLLECTION_TEMP)
        # Por default, una reservación debe llevar al menos un turno y al menos un piloto
        # TurnModel.add(reservation, {"schedule": "00", "turn_number": 0, "positions": {}, "date": None})
        # PilotModel.add(reservation, {'name': 'Piloto 1'})
        session['reservation'] = reservation._id
        return reservation

    @classmethod
    def update(cls, reservation, type):
        from app.models.qrs.qr import QR

        reservation.type = type
        reservation.update_mongo(COLLECTION_TEMP)
        #print(QR.remove_reservations_qrs())
        #QR.create(reservation)
        return reservation

    @classmethod
    def get_by_id(cls, _id, collection):
        """
        Returns the reservation object with the given id, or raises an exception if that reservation was not found
        :param _id: ID of the reservation to find
        :param collection: DB that contains all the reservations
        :return: Reservation object
        """
        reservation = Database.find_one(collection, {'_id': _id})
        if reservation:
            return cls(**reservation)
        raise ReservationNotFound("La reservación con el ID dado no existe.")

    @classmethod
    def remove_temporal_reservations(cls):
        for temp_reservation in Database.find(COLLECTION_TEMP, {}):
            reservation = cls(**temp_reservation)
            now = datetime.datetime.now().astimezone(get_localzone())
            delta = now - reservation.date
            if delta > TIMEOUT:
                reservation.delete_from_mongo(COLLECTION_TEMP)
