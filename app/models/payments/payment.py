import os
import requests
import json
import datetime

from tzlocal import get_localzone

from app.models.promos.errors import PromotionUsed
from app.models.promos.promotion import Promotion as PromoModel
from app.models.promos.constants import COLLECTION as PROMO_COLLECTION
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION
from app.models.users.user import User
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
    def parse_card(new_card):
        """
        Parses the information of the new card to be processed.
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

        if len(str(new_card.get("number"))) != 16:
            raise TokenisationFailed("El numero de la tarjeta es invalido.")
        auth = requests.get(URL)
        if auth.status_code == 200:
            token = requests.post(URL_TOKEN, params={}, data=json.dumps(card_info), headers=HEADERS)
            obj_token = json.loads(token.text)
            if obj_token.get("error") == 1:
                raise TokenisationFailed(obj_token.get("detail"))
            new_card["number"] = obj_token["card"]
            new_card["token"] = obj_token["token"]
            new_card["year"] = new_card.get("year")[-2:]
            card = cls(**new_card)
            return card
        raise TokenisationFailed("No fue posible tokenizar la tarjeta. Contacte al administrador.")


class Payment(BaseModel):
    def __init__(self, status, payment_method, payment_type, amount=None, license_price=None, turns_price=None,
                 promo=None, date=None, etomin_number=None, id_reference=None, _id=None):
        self.status = status
        self.payment_method = payment_method
        self.payment_type = payment_type
        self.amount = amount
        self.license_price = license_price
        self.turns_price = turns_price
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
        promo = None
        if promo_id:
            promo = PromoModel.get_promos(promo_id)[0]
            if not promo.status:
                raise PromotionUsed("Esta promoción ya fue utilizada por otro usuario.")

        payment = cls(**new_payment)

        location = reservation.location
        licensed_pilots = [pilot.licensed for pilot in reservation.pilots].count(True)
        license_price = licensed_pilots * location.type.get('LICENCIA')

        # Modificar para Sucursal Tlalnepantla
        # pues tiene un tercer tipo que no se considera en reservation.type
        if reservation.type == "Adultos":
            prices = location.type.get('GOKART')
        else:
            prices = location.type.get('CADET')

        prices_size = len(prices)
        turns_size = len(reservation.turns)
        turns_price = cls.calculate_turns_price(turns_size, prices_size, prices)
        payment.turns_price = turns_price

        if promo and promo.type == 'Carreras':
            turns_size -= promo.value
            former_turns_price = turns_price
            if turns_size > 0:
                turns_price = cls.calculate_turns_price(turns_size, prices_size, prices)
                promo.discount = former_turns_price - turns_price
            else:
                turns_price = 0
                promo.discount = former_turns_price - turns_price

        amount = license_price + turns_price

        if promo and promo.type == 'Descuento':
            promo.discount = amount * (promo.value / 100)
            amount -= promo.discount

        params = cls.build_etomin_params(user, payment, new_payment, amount, etomin_number)

        if promo and promo.type == 'Reservación':
            promo.discount = amount
            return cls.commit_reservation_payment(payment, 0, license_price, reservation, promo)
        else:
            if new_payment.get('payment_type') == 'Etomin':
                auth = requests.get(URL)
                if auth.status_code == 200:
                    obj = json.loads(auth.text)
                    params["transaction"]["device_session_id"] = obj["session_id"]
                    charge = requests.post(URL_CHARGE, params={}, data=json.dumps(params), headers=HEADERS)
                    obj_charge = json.loads(charge.text)
                    if int(obj_charge.get("error")) == 0:
                        payment.id_reference = obj_charge.get("authorization_code")
                        payment.etomin_number = obj_charge.get("card_token")
                        return cls.commit_reservation_payment(payment, amount, license_price, reservation, promo)
                    else:
                        payment.status = "RECHAZADO"
                        payment.etomin_number = etomin_number
                        raise PaymentFailed(obj_charge.get("message"))
            else:
                return cls.commit_reservation_payment(payment, amount, license_price, reservation, promo)

    @staticmethod
    def calculate_turns_price(turns_size, prices_size, prices):
        if turns_size != 3:
            return prices[prices_size - 1] * (turns_size // prices_size) + prices[turns_size % prices_size - 1]
        else:
            return prices[prices_size - 1]

    @staticmethod
    def build_etomin_params(user, payment, new_payment, amount, etomin_number):
        params = {}
        if new_payment.get('payment_type') == 'Etomin':
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
    def commit_reservation_payment(payment, amount, license_price, reservation: Reservation, promo):
        payment.status = "APROBADO"
        payment.amount = amount
        payment.license_price = license_price
        payment.date = datetime.datetime.now().astimezone(get_localzone())
        # Cambiar el status de la promoción utilizada
        if promo:
            promo.status = False
            promo.update_mongo(PROMO_COLLECTION)
        payment.promo = promo
        reservation.payment = payment
        # Guardar en la coleccion de reservaciones reales
        reservation.save_to_mongo(COLLECTION)
        # Borrar de la coleccion de reservaciones temporales
        reservation.delete_from_mongo(COLLECTION_TEMP)
        # Nulificar las fechas tentativas de reservacion
        for turn in reservation.turns:
            TurnModel.remove_allocation_dates(reservation, turn)
        return payment
