import os
import requests
import json
import datetime

from tzlocal import get_localzone
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
            card = cls(**new_card)
            return card
        raise TokenisationFailed("No fue posible tokenizar la tarjeta. Contacte al administrador.")


class Payment(BaseModel):
    def __init__(self, status, payment_method, amount=None, date=None, etomin_number=None, id_reference=None, _id=None):
        self.status = status
        self.payment_method = payment_method
        self.amount = amount
        self.etomin_number = etomin_number
        self.date = date
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
        card = Card.tokenise_card(new_card)

        new_payment["status"] = "PENDIENTE"

        etomin_number = card.token

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
        if turns_size != 3:
            turns_price = prices[prices_size - 1] * (turns_size // prices_size) + prices[turns_size % prices_size - 1]
        else:
            turns_price = prices[prices_size - 1]
        amount = license_price + turns_price
        print(license_price, " ", turns_price)
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

        auth = requests.get(URL)
        if auth.status_code == 200:
            obj = json.loads(auth.text)
            params["transaction"]["device_session_id"] = obj["session_id"]
            charge = requests.post(URL_CHARGE, params={}, data=json.dumps(params), headers=HEADERS)
            obj_charge = json.loads(charge.text)
            if int(obj_charge.get("error")) == 0:
                payment.status = "APROBADO"
                payment.amount = amount
                payment.date = datetime.datetime.now().astimezone(get_localzone())
                payment.id_reference = obj_charge.get("authorization_code")
                payment.etomin_number = obj_charge.get("card_token")
                new_payment["status"] = "APROBADO"
                reservation.payment = payment
                # Guardar en la colección de reservaciones reales
                reservation.save_to_mongo(COLLECTION)
                # Borrar de la colección de reservaciones temporales
                reservation.delete_from_mongo(COLLECTION_TEMP)
                # Nulificar las fechas tentativas de reservacion
                for turn in reservation.turns:
                    TurnModel.remove_allocation_dates(reservation, turn)
                return new_payment
            else:
                payment.status = "RECHAZADO"
                payment.etomin_number = etomin_number
                raise PaymentFailed(obj_charge.get("message"))
