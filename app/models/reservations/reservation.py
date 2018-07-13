from flask import session
import datetime
from tzlocal import get_localzone
from app.models.baseModel import BaseModel
from app.models.promos.promotion import Promotion as PromoModel, Coupons
from app.common.database import Database
from app.models.reservations.constants import COLLECTION_TEMP, TIMEOUT, COLLECTION as REAL_RESERVATIONS
from app.models.locations.constants import COLLECTION
from app.models.promos.constants import COLLECTION as PROMO_COLLECTION
from app.models.reservations.errors import ReservationNotFound, WrongReservationType

"""
This is the reservation model object which will be used to store the temporal and real collections of the user,
when they complete the process of reservation and the payment is processed.
"""


class Reservation(BaseModel):
    def __init__(self, type, date, location=None, payment=None, turns=list(), pilots=list(),
                 amount=None, license_price=None, turns_price=None, price_before_promo=None,
                 promo_id=None, coupon_id=None, discount=None, _id=None):
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
        try:
            self.payment = Payment(**payment) if payment else payment
        except TypeError:
            pass
        self.amount = amount
        self.license_price = license_price
        self.turns_price = turns_price
        self.price_before_promo = price_before_promo
        self.promo_id = promo_id
        self.coupon_id = coupon_id
        self.discount = discount

    @classmethod
    def add(cls, new_reservation):
        """
        Adds a new reservation to the Temporal Reservation Collection, when the user starts the process
        :param new_reservation: Reservation object with user information
        :return: Reservation object
        """
        from app.models.turns.turn import Turn as TurnModel
        from app.models.pilots.pilot import Pilot as PilotModel
        from app.models.locations.location import Location as LocationModel

        id_location = new_reservation.pop('id_location')
        location = Database.find_one(COLLECTION, {'_id': id_location})
        now = datetime.datetime.now().astimezone(get_localzone())
        reservation = cls(**new_reservation, date=now)
        # print(reservation.date)
        reservation.location = LocationModel(**location)
        if reservation.type != "Niños" and reservation.type != "Adultos":
            raise WrongReservationType("Error en el tipo de reservacion. Solo puede ser 'Adultos' o 'Niños'.")
        reservation.save_to_mongo(COLLECTION_TEMP)
        # Por default, una reservacion debe llevar al menos un turno y al menos un piloto
        # TurnModel.add(reservation, {"schedule": "00", "turn_number": 0, "positions": {}, "date": None})
        # PilotModel.add(reservation, {'name': 'Piloto 1'})
        session['reservation'] = reservation._id
        return reservation

    @classmethod
    def update(cls, reservation, type):
        from app.models.qrs.qr import QR
        from app.models.pilots.pilot import AbstractPilot
        reservation.type = type
        reservation.update_mongo(COLLECTION_TEMP)
        # QR.remove_reservation_qrs()
        # QR.create(reservation)
        # AbstractPilot.remove_allocated_pilots()
        return reservation

    @staticmethod
    def delete(reservation_id):
        """
        Removes from the Collection the given reservation
        :param reservation_id: The id of the reservation to be deleted from the collection
        :return: None
        """
        try:
            reservation = Reservation.get_by_id(reservation_id, COLLECTION_TEMP)
            reservation.delete_from_mongo(COLLECTION_TEMP)
        except ReservationNotFound:
            reservation = Reservation.get_by_id(reservation_id, REAL_RESERVATIONS)
            reservation.delete_from_mongo(REAL_RESERVATIONS)

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
        raise ReservationNotFound("La reservacion con el ID dado no existe.")

    @classmethod
    def remove_temporal_reservations(cls):
        for temp_reservation in Database.find(COLLECTION_TEMP, {}):
            reservation = cls(**temp_reservation)
            now = datetime.datetime.now().astimezone(get_localzone())
            delta = now - reservation.date
            if delta > TIMEOUT:
                reservation.delete_from_mongo(COLLECTION_TEMP)

    def calculate_price(self):
        from app.models.payments.payment import Payment
        location = self.location
        licensed_pilots = [pilot.licensed for pilot in self.pilots].count(True)
        license_price = licensed_pilots * location.type.get('LICENCIA')
        # Modificar para Sucursal Tlalnepantla
        # pues tiene un tercer tipo que no se considera en reservation.type
        if self.type == "Adultos":
            prices = location.type.get('GOKART')
        else:
            prices = location.type.get('CADET')
        prices_size = len(prices)
        turns_size = len(self.turns)
        turns_price = Payment.calculate_turns_price(turns_size, prices_size, prices)

        self.license_price = license_price
        self.turns_price = turns_price
        self.amount = license_price + turns_price
        self.update_mongo(COLLECTION_TEMP)
        return self

    def insert_promo(self, promo_id):
        promotion = PromoModel.find_promotion(promo_id)
        promo = PromoModel(**promotion.get('promo'))
        coupon = Coupons(**promotion.get('coupon'))
        self.promo_id = promo._id
        self.coupon_id = coupon._id

        from app.models.payments.payment import Payment
        location = self.location
        licensed_pilots = [pilot.licensed for pilot in self.pilots].count(True)
        license_price = licensed_pilots * location.type.get('LICENCIA')
        if self.type == "Adultos":
            prices = location.type.get('GOKART')
        else:
            prices = location.type.get('CADET')
        prices_size = len(prices)
        turns_size = len(self.turns)
        turns_price = Payment.calculate_turns_price(turns_size, prices_size, prices)
        self.price_before_promo = license_price + turns_price
        if promotion.get('promo').get('type') == 'Carreras':
            turns_size -= promotion.get('promo').get('value')
            former_turns_price = turns_price
            if turns_size > 0:
                turns_price = Payment.calculate_turns_price(turns_size, prices_size, prices)
                self.discount = former_turns_price - turns_price
            else:
                turns_price = 0
                self.discount = former_turns_price - turns_price
        amount = license_price + turns_price
        if promotion.get('promo').get('type') == 'Descuento':
            self.discount = amount * (promotion.get('promo').get('value') / 100)
            amount -= self.discount
        elif promotion.get('promo').get('type') == 'Reservación':
            self.discount = amount
            amount = 0
        promo.update_mongo(PROMO_COLLECTION)
        self.license_price = license_price
        self.turns_price = turns_price
        self.amount = amount
        self.update_mongo(COLLECTION_TEMP)
        return self
