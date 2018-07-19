import datetime

from tzlocal import get_localzone

from app import Database
from app.models.baseModel import BaseModel
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.pilots.errors import PilotNotFound
from app.models.pilots.constants import COLLECTION as PILOTS
from app.models.reservations.constants import COLLECTION_TEMP, TIMEOUT
from app.models.dates.constants import COLLECTION
from app.models.reservations.reservation import Reservation
from app.models.dates.date import Date as DateModel

"""
This is the pilot model object which holds the information of the pilot if they have a licence.
"""


class Pilot(BaseModel):
    def __init__(self, name, licensed, last_name, email, location,
                 birth_date, postal_code, nickname, city, _id=None):
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
        pilot = cls(**new_pilot, _id=new_pilot.get('email'))
        pilot.update_mongo(PILOTS)
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

    @staticmethod
    def send_confirmation_message(reservation: Reservation, qr_code):
        """
        Sends an email to the reservation pilots with the summary of their turns
        :param qr_code:
        :param reservation: Reservation object
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        for pilot in reservation.pilots:
            if pilot.licensed:
                email = Email(to=pilot.email, subject='Confirmación de reservación', qr_code=qr_code)
                turns_detail = ""
                for turn in reservation.turns:
                    turns_detail += "<p>" + turn.schedule + " hrs - Turno " + turn.turn_number + "</p>"
                    for key in turn.positions:
                        for driver in reservation.pilots:
                            if driver._id == turn.positions.get(key):
                                turns_detail += "<p>Posición " + key[-1] + ": " + driver.name + "</p>"
                    turns_detail += "<br>"

                pilots_detail = ""
                pilots_detail += "<p>Nombre: " + pilot.name + "</p>"
                pilots_detail += "<p>Apellido: " + pilot.last_name + "</p>"
                pilots_detail += "<p>Apodo: " + pilot.nickname + "</p>"
                pilots_detail += "<br>"

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
                           "En sus marcas. Listos. ¡Fuera!".format(pilot.name, reservation._id,
                                                                   reservation.location.name,
                                                                   reservation.date.strftime("%Y-%m-%d"),
                                                                   turns_detail, pilots_detail,
                                                                   reservation.payment.amount))

                email_html = """
                <html>
                <head>
                  <meta charset='utf-8' />
                  <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                  <title>GoKartMania</title>
                  <meta name='viewport' content='width=device-width, initial-scale=1'>
                  <link rel='stylesheet' type='text/css' media='screen' href='main.css' />
                  <script src='main.js'></script>
                  <style>
                      @import url('https://fonts.googleapis.com/css?family=Open+Sans:100,300,400,700');
                      @import url('https://fonts.googleapis.com/css?family=Roboto+Slab:100,300,400,700');
                    body {
                      font-family: 'Open Sans', sans-serif;
                    		margin-top: 0px;
                			margin-right: 0px;
                			margin-bottom: 0px;
                			margin-left: 0px;
                			color: white;
                    }
                    span {
                        color: white;
                    }
                    .primary {
                      color: #B9261A;
                    }
                  </style>
                </head>
                <body>

                  <table  border='0' cellpadding='0' cellspacing='0' height='100%' width='100%'>
                    <tr>
                      <td  align='center' valign='top'>
                        <table style='background-color: black;' border='0' cellpadding='20' cellspacing='0' width='600'>
                          <tr>
                            <td  align='center' valign='top' style='padding-bottom: 0px;'>
                              <table border='0' cellpadding='20' cellspacing='0' width='100%'>
                                <tr>
                                  <td align='center' valign='top' style='padding-top: 0px;'>
                                    <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                                      <tr>
                                        <td>
                                          <table>
                                            <tr>
                                              <td style='text-align:center;' align='center'>
                                                <a href='http://gokartmania.com.mx/'>
                                                  <img style='padding-left:110px;' src='http://138.197.209.15/assets/logoBlanco.png'>
                                                  <a/>
                                              </td>
                                            </tr>
                                          </table>
                                        </td>
                                      </tr>
                                    </table>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                          <tr>
                            <td style='background-color: #B9261A; height:10px;'></td>
                          </tr>
                          <tr>
                            <td align='center' valign='top' style='padding-top: 0px;'>
                              <table border='0' cellpadding='20' cellspacing='0' width='100%'>
                                <tr>
                                  <td align='center' valign='top' style='padding-top: 0px;'>
                                    <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                                      <tr>
                                        <td align='left' style='padding-top: 0px !important; font-weight: 700; padding-bottom:15px; font-size: 20px; color: white'>
                                          <br>"""
                email_html += """
                                           <p style='font-size:28px;'>¡Hola <span class='primary'>{}</span>!</p>""".format(pilot.name)
                email_html += """
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>
                                          <table width="100%">
                                            <tr>
                                              <td align="left" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white">
                                                 Gracias por tu compra en GoKartMania. <br> A continuación se desglosan los datos de su <span class="primary">compra</span>.
                                                  <p>
                                                    <span style="font-weight: 700;">Número de confirmación:</span> <span class="primary">{}</span></p>
                                                  <p>
                                                    <span style="font-weight: 700;">Ubicación:</span> <span class="primary">{}</span></p>
                                                  <p>
                                                    <span style="font-weight: 700;">Fecha:</span> <span class="primary">{}</span></p>
                                                  <p>""".format(reservation._id, reservation.location.name,
                                                                reservation.date.strftime("%Y-%m-%d"))
                email_html += """
                                                    <span style="font-weight: 700;">Detalle de los turnos:</span></p>
                                                    <div style="padding-left:25px">
                                                      {}
                                                    </div>""".format(turns_detail)
                email_html += """
                                                  <p>
                                                    <span style="font-weight: 700;">Tus datos:</span></p>
                                                    <div style="padding-left:25px; color: white;">
                                                      {}
                                                    </div>""".format(pilots_detail)
                qr_url = "http://138.197.209.15/qr/" + qr_code
                email_html += """
                                                  <p>
                                                    <span align="center" style="font-weight: 700;">Presenta en taquilla el siguiente <span class="primary">código QR</span> para comenzar tu carrera.</span></p>
                                              </td>
                                            </tr>
                                          </table>
                                          <br />
                                          <td>
                                      </tr>
                                      <tr>
                                        <td>
                                          <table width="100%">
                                            <tr>
                                              <td align="center" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white; text-align: center;">
                                                <img src={} alt='QR Code' />
                                                <br>
                                                <br>
                                                <span style="font-weight: 700; font-size: 32px; text-align: center;">En sus marcas. Listos.
                                                  <span class="primary">¡Fuera!</span>
                                                </span>
                                              </td>
                                            </tr>
                                          </table>
                                          <br />
                                          <td>
                                      </tr>
                                    </table>
                                    </td>
                                </tr>

                              </table>
                              </td>
                          </tr>
                              <tr>
                                <td style="background-color: #B9261A; height:10px;"></td>
                              </tr>
                        </table>
                        </td>
                    </tr>
                  </table>

                </body>
                </html>
                        """.format(qr_url)

                email.html(email_html)
                try:
                    email.send()
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
        timeout = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
        Database.DATABASE[COLLECTION].update_many({},
                                                  {'$pull': {'schedules.$[].turns.$[].pilots': {
                                                      'allocation_date': {'$lte': timeout}}}})

        Database.DATABASE[COLLECTION].update_many({},
                                                  {'$set': {'schedules.$[].turns.$[tu].type': None}},
                                                  array_filters=[{'tu.pilots': []}])
