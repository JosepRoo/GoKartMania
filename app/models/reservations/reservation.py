from flask import session
import datetime
from bson import CodecOptions
from app.models.baseModel import BaseModel
from app.models.dates.constants import MEXICO_TZ
from app.models.locations.errors import LocationNotFound
from app.models.promos.errors import InvalidPromotion
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
    def __init__(self, type, date, location=None, payment=None, turns=None, pilots=None,
                 amount=None, license_price=None, turns_price=None, price_per_race=None,
                 total_pilots=None, total_races=None, price_before_promo=None,
                 promo_id=None, coupon_id=None, discount=None, _id=None):
        from app.models.turns.turn import Turn
        from app.models.pilots.pilot import Pilot
        from app.models.payments.payment import Payment
        from app.models.locations.location import Location
        super().__init__(_id)
        self.type = type
        self.date = date
        self.location = Location(**location) if location else location
        self.turns = [Turn(**turn) for turn in turns] if turns is not None else list()
        self.pilots = [Pilot(**pilot) for pilot in pilots] if pilots is not None else list()
        try:
            self.payment = Payment(**payment) if payment else payment
        except TypeError:
            pass
        self.amount = amount
        self.license_price = license_price
        self.turns_price = turns_price
        self.price_per_race = price_per_race
        self.total_pilots = total_pilots
        self.total_races = total_races
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
        if location is None:
            raise LocationNotFound("La sucursal con este ID no fue encontrada.")
        now = datetime.datetime.now()
        aware_datetime = MEXICO_TZ.localize(now)
        reservation: Reservation = cls(**new_reservation, date=now)
        # print(reservation.date)
        reservation.location = LocationModel(**location)
        if reservation.type != "Niños" and reservation.type != "Adultos":
            raise WrongReservationType("Error en el tipo de reservacion. Solo puede ser 'Adultos' o 'Niños'.")
        reservation.save_to_mongo(COLLECTION_TEMP)
        # Por default, una reservacion debe llevar al menos un turno y al menos un piloto
        # TurnModel.add(reservation, {"schedule": "00", "turn_number": 0, "positions": {}, "date": None})
        # PilotModel.add(reservation, {'name': 'Piloto 1'})
        session['time_created'] = datetime.datetime.now()
        session['reservation'] = reservation._id
        return reservation

    def update(self, type):
        """
        Changes the type of the reservation (Kids or Adults)
        :param self: Reservation object
        :param type: Kids or adults
        :return: Reservation updated object
        """
        from app.models.qrs.qr import QR
        from app.models.pilots.pilot import AbstractPilot
        from app.models.dates.date import Date
        if type != "Niños" and type != "Adultos":
            raise WrongReservationType("Error en el tipo de reservacion. Solo puede ser 'Adultos' o 'Niños'.")
        self.type = type
        self.update_mongo(COLLECTION_TEMP)
        # QR.remove_reservation_qrs()
        # QR.create(self)
        # AbstractPilot.remove_allocated_pilots()
        # Reservation.remove_temporal_reservations()
        return self

    @staticmethod
    def delete(reservation_id) -> None:
        """
        Removes from the Collection the given reservation
        :param reservation_id: The id of the reservation to be deleted from the collection
        :return: None
        """
        try:
            reservation = Reservation.get_by_id(reservation_id, COLLECTION_TEMP)
            reservation.delete_from_mongo(COLLECTION_TEMP)
        except ReservationNotFound:
            try:
                reservation = Reservation.get_by_id(reservation_id, REAL_RESERVATIONS)
                reservation.delete_from_mongo(REAL_RESERVATIONS)
            except ReservationNotFound:
                raise ReservationNotFound("La reservacion con el ID dado no existe.")

    @classmethod
    def get_by_id(cls, _id, collection):
        """
        Returns the reservation object with the given id, or raises an exception if that reservation was not found
        :param _id: ID of the reservation to find
        :param collection: DB that contains all the reservations
        :return: Reservation object
        """
        if collection == "real_reservations":
            reservation = Database.find_one(collection, {'_id': _id}, tz_aware=False)
        else:
            reservation = Database.find_one(collection, {'_id': _id})
        if reservation:
            reservation_obj: Reservation = cls(**reservation)
            reservation_obj.date = datetime.datetime.strftime(reservation_obj.date, "%Y-%m-%d")
            return reservation_obj
        raise ReservationNotFound("La reservacion con el ID dado no existe.")

    @classmethod
    def remove_temporal_reservations(cls) -> None:
        """
        Removes those reservations from the Temp Reservation Collection that have expired their TIMEOUT
        :return: None
        """
        for temp_reservation in Database.find(COLLECTION_TEMP, {}):
            reservation = cls(**temp_reservation)
            now = datetime.datetime.now(MEXICO_TZ)
            delta = now - reservation.date
            if delta > TIMEOUT:
                reservation.delete_from_mongo(COLLECTION_TEMP)

    def calculate_price(self):
        """
        Pre-calculates the total price of the reservation and brings up it's information summary
        :return: Reservation object
        """
        from app.models.payments.payment import Payment
        location = self.location
        licensed_pilots = [pilot.licensed for pilot in self.pilots].count(True)
        license_price = licensed_pilots * location.type.get('LICENCIA')
        # This needs to be modified in Tlalnepantla for it has a third type Kartito, for babies
        if self.type == "Adultos":
            prices = location.type.get('GOKART')
        else:
            prices = location.type.get('CADET')
        prices_size = len(prices)

        self.total_races = len(self.turns)
        self.total_pilots = len(self.pilots)

        turns_price = Payment.calculate_turns_price(self.total_races, self.total_pilots, prices_size, prices)

        self.license_price = license_price
        self.turns_price = turns_price
        self.price_per_race = self.turns_price / self.total_races / self.total_pilots

        self.amount = self.license_price + self.turns_price
        self.update_mongo(COLLECTION_TEMP)

        if session.get('reservation_date') != datetime.datetime.strftime(self.date, "%Y-%m-%d"):
            self.date = datetime.datetime.strptime(session.get('reservation_date'), "%Y-%m-%d")
        return self

    def insert_promo(self, promo_id):
        """
        Inserts a promo in the current reservation, given a promo ID
        :param promo_id: ID of the promo to be applied
        :return: Updates reservation object or error message if ID was not found
        """
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
        pilots_size = len(self.pilots)
        turns_price = Payment.calculate_turns_price(turns_size, pilots_size, prices_size, prices)
        self.price_before_promo = self.amount

        # Ensure that the current reservation meets the promotion requirements
        if promo.at_least:
            if turns_size < promo.required_races:
                raise InvalidPromotion("Esta promoción solo es válida para reservaciones con al menos "
                                       f"{promo.required_races} turnos.")
        else:
            if turns_size != promo.required_races:
                raise InvalidPromotion("Esta promoción solo es válida para reservaciones con exactamente "
                                       f"{promo.required_races} turnos.")

        # Decreases the number of races to be paid
        if promotion.get('promo').get('type') == 'Carreras':
            turns_size -= promotion.get('promo').get('value')
            former_turns_price = self.amount
            if turns_size > 0:
                turns_price = Payment.calculate_turns_price(turns_size, pilots_size, prices_size, prices)
                self.discount = former_turns_price - turns_price
            else:
                turns_price = 0
                self.discount = former_turns_price - turns_price
        amount = self.price_before_promo
        # Decreases from the total amount the discount value
        if promotion.get('promo').get('type') == 'Descuento':
            self.discount = amount * (promotion.get('promo').get('value') / 100)
            turns_price -= self.discount
        # Sets the total amount to be paid to 0
        elif promotion.get('promo').get('type') == 'Reservación':
            self.discount = self.turns_price
            turns_price = 0
        promo.update_mongo(PROMO_COLLECTION)
        self.license_price = license_price
        self.turns_price = turns_price
        self.price_per_race = self.turns_price / self.total_races / self.total_pilots
        self.update_mongo(COLLECTION_TEMP)
        self.amount = self.license_price + self.turns_price
        return self

    @classmethod
    def get_reservations_in_time(cls, first_date, last_date):
        """
        Retrieves the information of every reservation completed (and payed) in a given date range
        :param first_date: The start date to be accounted
        :param last_date: The end date to be accounted
        :return: Array of reservation objects
        """
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(first_date, "%Y-%m-%d"))
        last_date = MEXICO_TZ.localize(datetime.datetime.strptime(last_date, "%Y-%m-%d"))
        expressions = list()
        expressions.append({'$match': {'date': {'$gte': first_date, '$lte': last_date}}})
        result = list(Database.DATABASE[REAL_RESERVATIONS].with_options(
            codec_options=CodecOptions(
                tz_aware=True, tzinfo=MEXICO_TZ)).aggregate(expressions))
        return [cls(**reservation) for reservation in result]
