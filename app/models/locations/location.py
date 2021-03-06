from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.locations.constants import COLLECTION
from app.models.admins.constants import COLLECTION as ADMINS, SUPERADMINS
from app.models.locations.errors import LocationNotFound
from app.models.users.user import User

"""
This is the location model object which will be used to append new locations to both the reservation
and the schedule, depending the POST method.
"""


class Location(BaseModel):
    from app.models.reservations.reservation import Reservation

    def __init__(self, name, type, _id=None):
        super().__init__(_id)
        self.name = name
        self.type = type

    @classmethod
    def add(cls, new_location):
        """
        Inserts a new location to the collection of locations
        :param new_location: Location to be added to the Location collection
        :relocation: A brand new location object
        """
        location: Location = cls(**new_location)
        location.save_to_mongo(COLLECTION)
        return location

    @classmethod
    def get_locations(cls, _id=None):
        """
        Fetches a list of the all the Location objects in the corresponding collection
        :param _id: The specific ID of a particular location object
        :return: List of Location objects or one specific Location object
        """
        if _id is None:
            return [cls(**location) for location in Database.find(COLLECTION, {})]
        else:
            location = Database.find_one(COLLECTION, {'_id': _id})
            if location is None:
                raise LocationNotFound("La ubicacion con el ID dado no existe.")
            return [cls(**location)]

    @classmethod
    def update(cls, updated_location):
        """
        Updates the information from the location with the given id.
        :param updated_location: The location data to be updated to the previous one
        :return: Location object with updated data
        """
        location = Database.find_one(COLLECTION, {'_id': updated_location['_id']})
        if location is None:
            raise LocationNotFound("La ubicacion con el ID dado no existe.")
        location: Location = cls(**updated_location)
        location.update_mongo(COLLECTION)
        return location

    @staticmethod
    def admins_send_reservation_info(user: User, reservation: Reservation, qr_code) -> None:
        """
        Sends an email to the current user with the summary of the reservation (all turns)
        :param user: User object
        :param qr_code: QR code path that will be displayed in the email
        :param reservation: Reservation object
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        admins = list()
        admins.extend(Database.find(ADMINS, {}))
        admins.extend(Database.find(SUPERADMINS, {}))
        recipients = [admin.get('email') for admin in admins]

        email = Email(recipients=recipients, subject='Confirmación de reservación')
        turns_detail = ""
        for turn in reservation.turns:
            turns_detail += "<p>" + turn.schedule + " hrs - Turno " + turn.turn_number + "</p>"
            for key in turn.positions:
                for pilot in reservation.pilots:
                    if pilot._id == turn.positions.get(key):
                        turns_detail += "<p>Posición " + key[-1] + ": " + pilot.name + "</p>"
            turns_detail += "<br>"

        pilots_detail = ""
        for pilot in reservation.pilots:
            pilots_detail += "<p>Nombre: " + pilot.name + "</p>"
            if pilot.email is not None:
                pilots_detail += "<p>Email: " + pilot.email + "</p>"
            if pilot.location is not None:
                pilots_detail += "<p>Sucursal: " + pilot.location + "</p>"
            if pilot.birth_date is not None:
                pilots_detail += "<p>Fecha de Nacimiento: " + pilot.birth_date + "</p>"
            if pilot.postal_code is not None:
                pilots_detail += "<p>Código Postal: " + pilot.postal_code + "</p>"
            if pilot.nickname is not None:
                pilots_detail += "<p>Nickname: " + pilot.nickname + "</p>"
            if pilot.city is not None:
                pilots_detail += "<p>Ciudad: " + pilot.city + "</p>"
            if pilot.licensed:
                pilots_detail += "<p>Este piloto desea adquirir licencia." + "</p>"
            else:
                pilots_detail += "<p>Este piloto ya cuenta con licencia." + "</p>"
            pilots_detail += "<br>"

        html = """
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
        html += """
                                               <p style='font-size:28px;'>¡Hola <span class='primary'>{}</span>!</p>""".format("GoKartMania")
        html += """
                                            </td>
                                          </tr>
                                          <tr>
                                            <td>
                                              <table width="100%">
                                                <tr>
                                                  <td align="left" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white">
                                                      A continuación se desglosan los datos de la reservación del cliente <span class="primary">{}</span>.
                                                      <p>
                                                        <span style="font-weight: 700;">Número de confirmación:</span> <span class="primary">{}</span></p>
                                                      <p>
                                                        <span style="font-weight: 700;">Ubicación:</span> <span class="primary">{}</span></p>
                                                      <p>
                                                        <span style="font-weight: 700;">Fecha:</span> <span class="primary">{}</span></p>
                                                      <p>
                                                        <span style="font-weight: 700;">Número telefónico:</span> <span class="primary">{}</span></p>
                                                      <p>""".format(user.name, reservation._id,
                                                                    reservation.location.name,
                                                                    reservation.date.strftime("%Y-%m-%d"),
                                                                    user.phone)
        html += """
                                                        <span style="font-weight: 700;">Detalle de los turnos:</span></p>
                                                        <div style="padding-left:25px">
                                                          {}
                                                        </div>""".format(turns_detail)
        html += """
                                                      <p>
                                                        <span style="font-weight: 700;">Pilotos:</span></p>
                                                        <div style="padding-left:25px; color: white;">
                                                          {}
                                                        </div>""".format(pilots_detail)
        html += """
                                                      <p>
                                                        <span style="font-weight: 700;">Desglose de la compra:</span>
                                                      </p>
                                                      <div style="padding-left:25px">
                                                        <p>
                                                          Costo de licencia: <span class="primary">${}</span>
                                                        </p>
                                                        <p>
                                                          Costo de las carreras: <span class="primary">${}</span>
                                                        </p>
                                                        <p>
                                                          Subtotal: <span class="primary">${}</span>
                                                        </p>""".format(reservation.license_price,
                                                                       reservation.turns_price,
                                                                       reservation.license_price + reservation.turns_price)
        if reservation.payment.promo:
            html += """
                                                        <p>
                                                          Descuento: <span class="primary">${}</span>
                                                        </p>""".format(reservation.discount)
        else:
            html += """
                                                        <p>
                                                          Descuento: <span class="primary">$0</span>
                                                        </p>"""
        html += """
                                                        <p>
                                                          Total: <span class="primary">${}</span>
                                                        </p>
                                                      </div>
                                                      <p>

                                                      </p>
                                                        <br>
                                                      <p>
                                                        <span align="center" style="font-weight: 700;">El siguiente <span class="primary">código QR</span> será presentado en taquilla para confirmar la carrera.</span>
                                                      </p>
                                                  </td>
                                                </tr>
                                              </table>
                                              <br />
                                              <td>
                                          </tr>""".format(reservation.amount)
        qr_url = "http://138.197.209.15/qr/" + qr_code
        html += """
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
        email.html(html)

        try:
            email.send_email()
        except EmailErrors as e:
            raise FailedToSendEmail(e)
