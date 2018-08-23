import os
import requests
import json
import datetime

from flask import session
from tzlocal import get_localzone

from app.models.promos.errors import PromotionUsed
from app.models.promos.promotion import Promotion as PromoModel
from app.models.promos.promotion import Coupons as CouponsModel
from app.models.promos.constants import COLLECTION as PROMO_COLLECTION
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.pilots.constants import COLLECTION as PILOTS
from app.models.users.user import User
from app.models.users.constants import COLLECTION as USER
from app.models.baseModel import BaseModel
from app.models.payments.constants import CURRENCY, PAYMENT_COUNTRY, URL, URL_CHARGE, URL_TOKEN, HEADERS
from app.models.payments.errors import PaymentFailed, TokenisationFailed
from app.models.reservations.reservation import Reservation
from app.models.turns.turn import Turn as TurnModel
from app.models.locations.location import Location

"""
This is the payment model object which holds the information of the payment to concrete a reservation.
"""


class Card(BaseModel):
    def __init__(self, number, name, token, month, year, _id=None):
        super().__init__(_id)
        self.number = number
        self.name = name
        self.token = token
        self.month = month
        self.year = year

    @staticmethod
    def parse_card(new_card) -> dict:
        """
        Parses the information of the new card to be processed.
        :new_card: The card information - Name, number, CVV, month, and year
        :return: A dictionary that etomin will process.
        """
        return {
            "card": {
                "cardholder": new_card.get("name"),
                "number": new_card.get("number"),
                "cvv": new_card.pop("cvv"),
                "expirationDate": new_card.get("month") + "/" + new_card.get("year")[-2:]
            }
        }

    @classmethod
    def tokenise_card(cls, new_card):
        """
        Uses Etomin API to tokenise a card given
        :param new_card: The new card to be processed and tokenised
        :return: A brand new card
        """
        card_info = cls.parse_card(new_card)

        if 17 <= len(str(new_card.get("number"))) <= 14:
            raise TokenisationFailed("El número de la tarjeta es inválido.")
        auth = requests.get(URL)
        if auth.status_code == 200:
            token = requests.post(URL_TOKEN, params={}, data=json.dumps(card_info), headers=HEADERS)
            obj_token = json.loads(token.text)
            if obj_token.get("error") == 1:
                raise TokenisationFailed(obj_token.get("detail"))
            new_card["number"] = obj_token["card"]
            new_card["token"] = obj_token["token"]
            new_card["year"] = new_card.get("year")[-2:]
            card: Card = cls(**new_card)
            return card
        raise TokenisationFailed("No fue posible tokenizar la tarjeta. Contacte al administrador.")


class Payment(BaseModel):
    def __init__(self, status, payment_method, payment_type,
                 promo=None, date=None, etomin_number=None, id_reference=None, _id=None):
        self.status = status
        self.payment_method = payment_method
        self.payment_type = payment_type
        self.etomin_number = etomin_number
        self.date = date
        self.promo = PromoModel(**promo) if promo else promo
        self.id_reference = id_reference
        super().__init__(_id)

    @classmethod
    def add(cls, user: User, reservation: Reservation, new_card, new_payment):
        """
        Adds a new payment to the given user.
        :param new_card: The new card to be processed
        :param user: User object
        :param reservation: Reservation object
        :param new_payment: The new payment to be added to the user
        :return: A brand new payment
        """

        if len(reservation.turns) == 0:
            raise PaymentFailed("Esta reservación no cuenta con ningúna carrera.")

        etomin_number = 0
        if new_payment.get('payment_type') == 'Etomin':
            card = Card.tokenise_card(new_card)
            etomin_number = card.token

        new_payment["status"] = "PENDIENTE"

        promo_id = new_payment.pop('promo_id')
        coupon_id = new_payment.pop('coupon_id')
        phone = new_payment.pop('phone')
        user.phone = phone
        promo = None
        coupon = None
        if promo_id:
            promo = PromoModel.get_promos(promo_id)[0]
            coupon = CouponsModel.get_coupon_by_id(promo_id, coupon_id)
            if not coupon.status:
                raise PromotionUsed("Este cupón ya fue utilizado el máximo número permitido de veces.")

        payment = cls(**new_payment)

        if promo and promo.type == 'Reservación':
            return cls.commit_reservation_payment(payment, 0, reservation.license_price, reservation, promo, coupon, user)
        else:
            if new_payment.get('payment_type') == 'Etomin':
                auth = requests.get(URL)
                if auth.status_code == 200:
                    params = cls.build_etomin_params(user, payment, new_payment, reservation.amount, etomin_number)
                    obj = json.loads(auth.text)
                    params["transaction"]["device_session_id"] = obj["session_id"]
                    charge = requests.post(URL_CHARGE, params={}, data=json.dumps(params), headers=HEADERS)
                    obj_charge = json.loads(charge.text)
                    if int(obj_charge.get("error")) == 0:
                        payment.id_reference = obj_charge.get("authorization_code")
                        payment.etomin_number = obj_charge.get("card_token")
                        return cls.commit_reservation_payment(payment, reservation.amount, reservation.license_price,
                                                              reservation, promo, coupon, user)
                    else:
                        payment.status = "RECHAZADO"
                        payment.etomin_number = etomin_number
                        raise PaymentFailed(obj_charge.get("message"))
            else:
                return cls.commit_reservation_payment(payment, reservation.amount, reservation.license_price,
                                                      reservation, promo, coupon, user)

    @staticmethod
    def calculate_turns_price(turns_size, prices_size, prices) -> int:
        """
        Calculates the total price of the turns depending on how many turns were selected, and the location
        :param turns_size: Total turns selected
        :param prices_size: The length of the array of prices of a certain location
        :param prices: The actual array containing the prices of a certain location
        :return: Price to be paid in terms of the turns
        """
        if turns_size != 3:
            return prices[prices_size - 1] * (turns_size // prices_size) + prices[turns_size % prices_size - 1]
        else:
            return prices[prices_size - 1]

    @staticmethod
    def build_etomin_params(user, payment, new_payment, amount, etomin_number) -> dict:
        """
        Takes into account the user, payment and etomin number data to parse etomin parameters
        :param user: User object with its data
        :param payment: Payment object used for the external reference
        :param new_payment: The payment containing the method
        :param amount: Total amount to be payed
        :param etomin_number: Etomin number (given by etomin api)
        :return: Etomin parse-ful parameters
        """
        params = {
            "public_key": os.environ.get("ETOMIN_PB_KEY"),
            "transaction": {
                "payer": {
                    "email": user.email
                },
                "order": {
                    "external_reference": payment._id
                },
                "payment": {
                    "amount": amount,
                    "payment_method": new_payment.get("payment_method"),
                    "currency": CURRENCY,
                    "payment_country": PAYMENT_COUNTRY,
                    "token": etomin_number
                },
                "payment_pending": False,
                "device_session_id": ""
            },
            "test": True
        }
        return params

    @staticmethod
    def commit_reservation_payment(payment, amount, license_price, reservation: Reservation, promo, coupon, user):
        """
        Attempts to concrete the payment taking into account the reservation, promo, and user information
        :param payment: Payment object
        :param amount: Total amount to be payed by the user
        :param license_price: The price only in in terms of the licence
        :param reservation: Reservation object
        :param promo: Promo object with information of use
        :param coupon: Instance of promo with more specific information
        :param user: User object
        :return: Completed and approved payment
        """
        payment.status = "APROBADO"
        payment.amount = amount
        payment.license_price = license_price
        payment.date = datetime.datetime.now().astimezone(get_localzone())
        if promo:
            # Cambiar el status de la promoción utilizada
            for c in promo.coupons:
                if c._id == coupon._id:
                    promo.coupons.remove(c)
                    coupon.date_applied = payment.date
                    coupon.copies_left -= 1
                    if coupon.copies_left == 0:
                        coupon.status = False
                    promo.coupons.append(coupon)
                    promo.update_mongo(PROMO_COLLECTION)
                    break
            del promo.coupons
            promo.coupon_applied = coupon._id
            payment.promo = promo
        reservation.payment = payment
        if session.get('reservation_date') != datetime.datetime.strftime(reservation.date, "%Y-%m-%d"):
            aware_datetime = get_localzone().localize(datetime.datetime.strptime(session.get('reservation_date'), "%Y-%m-%d"))
            reservation.date = aware_datetime
        # print(reservation.date)
        for pilot in reservation.pilots:
            pilot.update_mongo(PILOTS)
        # Guardar en la coleccion de reservaciones reales
        reservation.save_to_mongo(COLLECTION)
        # Borrar de la coleccion de reservaciones temporales
        reservation.delete_from_mongo(COLLECTION_TEMP)
        # Nulificar las fechas tentativas de reservacion
        for turn in reservation.turns:
            TurnModel.remove_allocation_dates(reservation, turn)
        # Agregar la reservación al usuario
        user.reservations.append(reservation._id)
        user.update_mongo(USER)
        return payment
