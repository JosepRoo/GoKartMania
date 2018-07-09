import datetime

from tzlocal import get_localzone

from app import Database
from app.models.baseModel import BaseModel
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.pilots.errors import PilotNotFound
from app.models.reservations.constants import COLLECTION_TEMP, TIMEOUT
from app.models.dates.constants import COLLECTION
from app.models.reservations.reservation import Reservation
from app.models.dates.date import Date as DateModel

"""
This is the pilot model object which holds the information of the pilot if they have a licence.
"""


class Pilot(BaseModel):
    def __init__(self, name, licensed, last_name=None, email=None, location=None,
                 birth_date=None, postal_code=None, nickname=None, city=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.birth_date = birth_date
        self.postal_code = postal_code
        self.nickname = nickname
        self.city = city
        self.licensed = licensed

    @classmethod
    def add(cls, reservation: Reservation, new_pilot):
        """
        Adds a new pilot to the given reservation party.
        :param reservation: Reservation object
        :param new_pilot: The new pilot to be added to the reservation
        :return: A brand new pilot
        """
        pilot = cls(**new_pilot)
        reservation.pilots.append(pilot)
        reservation.update_mongo(COLLECTION_TEMP)
        return pilot

    @staticmethod
    def get(reservation: Reservation, pilot_id):
        """
        Retrieves the information of the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be read from the reservation
        :return: The requested pilot
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                return pilot
        raise PilotNotFound("El piloto con el ID dado no existe")

    @classmethod
    def update(cls, reservation: Reservation, updated_pilot, pilot_id):
        """
        Updates the information from the pilot with the given id.
        :param reservation: Reservation object containing the array of pilots
        :param updated_pilot: The pilot data to be updated to the previous one
        :param pilot_id: the ID of the pilot to be updated
        :return: All the pilots of the current reservation, with updated data
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                new_pilot = cls(**updated_pilot, _id=pilot_id)
                reservation.pilots.remove(pilot)
                reservation.pilots.append(new_pilot)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.pilots
        raise PilotNotFound("El piloto con el ID dado no existe")

    @staticmethod
    def delete(reservation: Reservation, pilot_id):
        """
        Removes from the reservations array of pilots the pilot with the given id.
        :param reservation: Reservation object
        :param pilot_id: The id of the pilot to be deleted from the reservation
        :return: The remaining pilots of the reservation
        """
        for pilot in reservation.pilots:
            if pilot._id == pilot_id:
                reservation.pilots.remove(pilot)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.pilots
        raise PilotNotFound("El piloto con el ID dado no existe")

    def send_confirmation_message(self, reservation: Reservation, qr_code):
        """
        Sends an email to the reservation pilots with the summary of their turns
        :param qr_code:
        :param reservation: Reservation object
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        for pilot in reservation.pilots:
            if pilot.licensed:
                email = Email(to=pilot.email, subject='confirmacion de reservacion', qr_code=qr_code)
                # email = Email(to='areyna@sitsolutions.org', subject='confirmacion de reservacion', qr_code=qr_code)
                turns_detail = ""
                for turn in reservation.turns:
                    turns_detail += "<p>" + turn.schedule + " hrs - Turno " + turn.turn_number + "\n</p>"
                    for key in turn.positions:
                        if pilot._id == turn.positions.get(key):
                            turns_detail += "<p>Tu GoKart es el: " + key[-1] + "\n</p>"
                    turns_detail += "\n"

                pilots_detail = ""
                pilots_detail += "<p>Nombre: " + pilot.name + "\n</p>"
                pilots_detail += "<p>Apellido: " + pilot.last_name + "\n</p>"
                pilots_detail += "<p>Apodo: " + pilot.nickname + "\n</p>"
                pilots_detail += "\n"

                email.text("Estimado {}:\n"
                           "Gracias por usar el servicio de Reservaciones de GoKartMania.\n"
                           "A continuacion se desglosan los datos de su compra:\n\n"
                           "Numero de confirmacion:\n"
                           "{}\n\n"
                           "Ubicacion:\n"
                           "{}\n\n"
                           "Fecha:\n"
                           "{}\n\n"
                           "Detalle de los turnos:\n"
                           "{}\n"
                           "Tus datos:\n"
                           "{}\n"
                           "Total de la compra:\n"
                           "${}\n\n"
                           "Presenta en taquilla el codigo adjunto para comenzar tu carrera.\n\n"
                           "En sus marcas. Listos. ¡Fuera!".format(self.name, reservation._id,
                                                                   reservation.location.name,
                                                                   reservation.date.strftime("%Y-%m-%d"),
                                                                   turns_detail, pilots_detail,
                                                                   reservation.payment.amount))

                email.html("<html>"
                           "    <head>Tu reservacion.</head>"
                           "    <body>"
                           "        <h1>Estimado {}:\n</h1>"
                           "        <p>Gracias por usar el servicio de Reservaciones de GoKartMania.\n</p>"
                           "        <p>A continuacion se desglosan los datos de su compra:\n\n</p>"
                           "        <strong>Numero de confirmacion:\n</strong>"
                           "        <p>{}\n\n</p>"
                           "        <strong>Ubicacion:\n</strong>"
                           "        <p>{}\n\n</p>"
                           "        <strong>Fecha:\n</strong>"
                           "        <p>{}\n\n</p>"
                           "        <strong>Detalle de los turnos:\n</strong>"
                           "        {}\n"
                           "        <strong>Tus datos:\n</strong>"
                           "        {}\n"
                           "        <strong>Total de la compra:\n</strong>"
                           "        <p>${}\n\n</p>"
                           "        <p>Presenta en taquilla el codigo adjunto para comenzar tu carrera.\n\n</p>"
                           "        <p>En sus marcas. Listos. ¡Fuera!</p>"
                           "    </body>"
                           "</html>".format(self.name, reservation._id, reservation.location.name,
                                            reservation.date.strftime("%Y-%m-%d"), turns_detail, pilots_detail,
                                            reservation.payment.amount))

                try:
                    email.send()
                    return email
                except EmailErrors as e:
                    raise FailedToSendEmail(e)


class AbstractPilot(BaseModel):
    from app.models.turns.turn import AbstractTurn

    def __init__(self, position, allocation_date, _id=None):
        super().__init__(_id)
        self.position = position
        self.allocation_date = allocation_date

    @classmethod
    def add(cls, turn: AbstractTurn, new_pilot):
        """
        Adds a new pilot to the given abstract turn party
        :param turn: Abstract turn object
        :param new_pilot: The new pilot to be added to the turn
        :return: Pilot object
        """
        pilot = cls(**new_pilot)
        turn.pilots.append(pilot)
        return pilot

    @staticmethod
    def remove_allocated_pilots():
        """
        Removes the allocated date-schedule-turn-pilots that have already concluded their TIMEOUT
        :return: None
        """
        timeout = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        Database.DATABASE[COLLECTION].update_many({},
                                                  {'$pull': {'schedules.$[].turns.$[].pilots': {
                                                      'allocation_date': {'$lte': timeout}}}})

        Database.DATABASE[COLLECTION].update_many({},
                                                  {'$set': {'schedules.$[].turns.$[tu].type': None}},
                                                  array_filters=[{'tu.pilots': []}])
