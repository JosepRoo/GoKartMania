from flask import session
from app import Database
from app.common.utils import Utils
from app.models.baseModel import BaseModel
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.users.constants import COLLECTION
from app.models.users.errors import InvalidEmail

"""
In this user model the email will be used to identify each user although an _id will be created for each instance of it
"""


class User(BaseModel):
    from app.models.reservations.reservation import Reservation

    def __init__(self, email, name, reservations=None, phone=None, _id=None):
        super().__init__(_id)
        self.email = email
        self.name = name
        self.phone = phone
        self.reservations = reservations if reservations is not None else list()

    @classmethod
    def get_by_email(cls, email):
        """
        Attempts to find a user according to the given email
        :param email: The email to be found in the User Collection
        :return: Found User object
        """
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            user_obj: User = cls(**data)
            return user_obj

    @classmethod
    def register(cls, kwargs):
        """
        Registers a new user if the provided email was not found in the existing collection
        :param kwargs: Key word arguments that contain the new user information
        :return: User object
        """
        email = kwargs['email']
        if not Utils.email_is_valid(email):
            raise InvalidEmail("El email dado no tiene un formato válido.")
        user = User.get_by_email(email)
        if user is None:
            new_user: User = cls(**kwargs)
            new_user.save_to_mongo(COLLECTION)
        else:
            new_user: User = cls(**kwargs, _id=user._id)
            new_user.update_mongo(COLLECTION)
        return new_user

    def send_confirmation_message(self, reservation: Reservation, qr_code) -> None:
        """
        Sends an email to the current user with the summary of the reservation (all turns)
        :param qr_code: QR code path that will be displayed in the email
        :param reservation: Reservation object
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        email = Email(to=self.email, subject='Confirmación de reservación', qr_code=qr_code)

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
            if pilot.licensed:
                pilots_detail += "<p>Licencia: Sí" + "</p>"
            else:
                pilots_detail += "<p>Licencia: No" + "</p>"
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
                   "Pilotos:\n"
                   "{}\n"
                   "Total de la compra:\n"
                   "${}\n\n"
                   "Presenta en taquilla el codigo adjunto para comenzar tu carrera.\n\n"
                   "En sus marcas. Listos. ¡Fuera!".format(self.name, reservation._id,
                                                           reservation.location.name,
                                                           reservation.date.strftime("%Y-%m-%d"),
                                                           turns_detail, pilots_detail, reservation.amount))
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
                           <p style='font-size:28px;'>¡Hola <span class='primary'>{}</span>!</p>""".format(self.name)
        email_html += """
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <table width="100%">
                            <tr>
                              <td align="left" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white">
                                 Gracias por tu compra en GoKartMania. <br> A continuación se desglosan los datos de su <span class="primary">reservación</span>.
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
                                    <span style="font-weight: 700;">Pilotos:</span></p>
                                    <div style="padding-left:25px; color: white;">
                                      {}
                                    </div>""".format(pilots_detail)
        email_html += """
                                  <p>
                                    <span style="font-weight: 700;">Desglose de tu compra:</span>
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
            email_html += """
                                    <p>
                                      Descuento: <span class="primary">${}</span>
                                    </p>""".format(reservation.discount)
        else:
            email_html += """
                                    <p>
                                      Descuento: <span class="primary">$0</span>
                                    </p>"""
        email_html += """
                                    <p>
                                      Total: <span class="primary">${}</span>
                                    </p>
                                  </div>
                                  <p>
                                  
                                  </p>
                                    <br>
                                  <p>
                                    <span align="center" style="font-weight: 700;">Presenta en taquilla el siguiente <span class="primary">código QR</span> para comenzar tu carrera.</span>
                                  </p>
                                    
                              </td>
                            </tr>
                          </table>
                          <br />
                          <td>
                      </tr>""".format(reservation.amount)
        qr_url = "http://138.197.209.15/qr/"+qr_code
        email_html += """
                      <tr>
                        <td>
                          <table width="100%">
                            <tr>
                              <td align="center" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white; text-align: center;">
                                <img src={} alt='QR Code' />
                                <br>
                                <br>
                                <p>Favor de llegar al menos 20 minutos previos a la hora de tu reservación.</p>
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
