import datetime
import os

from flask import session
from tzlocal import get_localzone

from app import Database
from app.common.utils import Utils
from app.models.admins.errors import InvalidEmail, InvalidLogin, AdminNotFound, ReportFailed
from app.models.baseModel import BaseModel
from app.models.admins.constants import COLLECTION, SUPERADMINS
from app.models.dates.constants import COLLECTION as DATES
from app.models.pilots.errors import PilotNotFound
from app.models.pilots.pilot import Pilot
from app.models.recoveries.errors import UnableToRecoverPassword
from app.models.recoveries.recovery import Recovery
from app.models.reservations.constants import COLLECTION as RESERVATIONS
from app.models.pilots.constants import COLLECTION as PILOTS
from app.models.dates.date import Date
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.promos.promotion import Promotion
from app.models.reservations.errors import ReservationNotFound
from config import basedir

"""
This is the admin user model that will be used to manage different dashboard information and analytics
"""


class Admin(BaseModel):
    def __init__(self, email, name, password, _id=None):
        super().__init__(_id)
        self.email = email
        self.name = name
        self.password = password

    @classmethod
    def get_by_email(cls, email):
        """
        Attempts to find an admin according to the given email
        :param email: The email to be found in the Admin Collection
        :return: Found Admin object
        """
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            admin: Admin = cls(**data)
            return admin
        else:
            data = Database.find_one(SUPERADMINS, {"email": email})
            if data is not None:
                admin: Admin = cls(**data)
                return admin

    @classmethod
    def admin_login(cls, data):
        """
        Login the user admin given its name, email, and password, or throws Incorrect Credentials error
        :param data: The admin credentials
        :return: Admin object
        """
        email = data.get('email')
        password = data.get('password')
        admin = Admin.get_by_email(email)
        if admin and Utils.check_hashed_password(password, admin.password):
            if admin.email == 'javierj@gokartmania.com.mx':
                session['sudo'] = admin._id
            session['admin_id'] = admin._id
            return admin
        else:
            raise InvalidLogin("Credenciales incorrectas")

    def send_recovery_message(self):
        """
        Sends an email to the given admin with the instructions to change their password
        :param self: Admin
        :return: POST method requesting an email to be sent to the admin
        """
        recovery = Recovery(admin_email=self.email)
        recovery.save_to_mongo()
        # email = Email(to=self.email, subject='Recuperación de contraseña', qr_code=None)
        email: Email = Email(to='areyna@sitsolutions.org', subject='Recuperación de contraseña', qr_code=None)
        email.text(
            f"Hola, {self.name}:\nHas recibido este correo electrónico porque recientemente solicitaste restablecer "
            "la contraseña asociada a tu cuenta de GoKartMania. Si no solicitaste este cambio, puedes hacer caso "
            "omiso de este correo.\n\nCopia y pega el siguiente enlace en tu navegador de internet para restablecer tu contraseña:\n"
            f"reservas.gokartmania.com.mx/#/admin/reset_password/{recovery._id}\n\nSaludos,\nEl equipo de GoKartMania.")

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
        email_html += f"""
                                   <p style='font-size:28px;'>Recuperación de <span class='primary'>contraseña</span>.</p>
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <table width="100%">
                                    <tr>
                                      <td align="left" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white">
                                          <p>
                                            Hola, {self.name}:
                                          </p>
                                          <p>
                                            Has recibido este correo electrónico porque recientemente solicitaste
                                            restablecer la contraseña asociada a tu cuenta de GoKartMania. Si no
                                            solicitaste este cambio, puedes hacer caso omiso de este correo.
                                          </p>
                                          <br>
                                          <p>
                                            Copia y pega el siguiente enlace en tu navegador de internet para
                                            restablecer tu contraseña:
                                          </p>
                                          <p>
                                            <a href='http://gokartmania.com.mx/#/admin/reset_password/{recovery._id}'>
                                              <span style="font-weight: 700;">reservas.gokartmania.com.mx/#/admin/reset_password/</span> <span class="primary">{recovery._id}</span>
                                            </a>
                                          </p>
                                          <p>
                                            <span style="font-weight: 700;">Saludos, </span>
                                          </p>
                                          <p>
                                            <span style="font-weight: 700;">El equipo de </span>
                                            <span class="primary">GoKartMania</span>.
                                          </p>
                                      </td>
                                    </tr>
                                  </table>
                                  <br>
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
                """

        email.html(email_html)
        email.send()
        return email

    def set_password(self, password) -> None:
        """
        Creates a new password for the admin and updates the previous one
        :param password: password to be updated
        :return: None
        """
        self.password = Utils.hash_password(password)

    @staticmethod
    def recover_password(recovery_id, email, new_password):
        """
        Updates the password of the admin with the given email to the database, provided a recovery ID
        :param recovery_id: token to ensure a safe recovery
        :param email: email of the admin to be found
        :param new_password: password to be updated
        :return: Admin object
        """
        if Recovery.recover_in_db(recovery_id):
            admin = Admin.get_by_email(email)
            admin.set_password(new_password)
            admin.update_mongo(COLLECTION)
            return admin
        else:
            raise UnableToRecoverPassword("No se pudo hacer la recuperación de la contraseña.")

    @staticmethod
    def send_alert_message(promo: Promotion) -> None:
        """
        Sends an email to the super-admin in order to authorise a given promotion
        :param promo: Promotion object containing the information of the promo to be confirmed
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        email = Email(to='javierj@gokartmania.com.mx', subject='Confirmación de promoción', qr_code=None)
        # email = Email(to='areyna@sitsolutions.org', subject='Confirmación de promoción', qr_code=None)

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
                           <p style='font-size:28px;'>Autorización de <span class='primary'>promoción</span>.</p>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <table width="100%">
                            <tr>
                              <td align="left" style="font-weight: 400; padding-bottom:15px; font-size: 20px; color: white">
                                  Nuestro sistema ha detectado que un empleado de GoKartMania ha intentado
                                  introducir una promoción con los siguientes detalles: 
                                  <p>
                                    <span style="font-weight: 700;">Número de cupones:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Fecha de inicio:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Fecha de término:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Tipo de promoción:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Nombre del encargado:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Fecha de creación:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Descripción:</span> <span class="primary">{}</span></p>
                                  <p>
                                    <span style="font-weight: 700;">Valor de la promo:</span> <span class="primary">{}</span></p>
                                  <p>""".format(promo.existence, promo.start_date, promo.end_date, promo.type,
                                                promo.creator,
                                                datetime.datetime.strftime(promo.created_date, '%d-%m-%Y %H:%M'),
                                                promo.description, promo.value)
        email_html += """
                                  <p>
                                    <span align="center" style="font-weight: 700;">Entra en el siguiente <a href='http://gokartmania.com.mx/#/admin/promos/{}'>enlace</a> para confirmar, modificar o desactivar esta promoción.</span>
                                  </p>
                              </td>
                            </tr>
                          </table>
                          <br>
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
        """.format(promo._id)

        email.text("Autorización de promoción.\n"
                   "Nuestro sistema ha detectado que un empleado de GoKartMania ha intentado "
                   "introducir una promoción con los siguientes detalles:\n\n"
                   "Numero de cupones:\n"
                   "{}\n"
                   "Fecha de inicio:\n"
                   "{}\n"
                   "Fecha de término:\n"
                   "{}\n"
                   "Tipo de promoción:\n"
                   "{}\n"
                   "Nombre del encargado:\n"
                   "{}\n"
                   "Fecha de creación:\n"
                   "{}\n"
                   "Descripción:\n"
                   "{}\n"
                   "Valor de la promo::\n"
                   "${}\n\n"
                   "Presenta en taquilla el codigo adjunto para comenzar tu carrera.\n\n"
                   "En sus marcas. Listos. ¡Fuera!".format(promo.existence, promo.start_date, promo.end_date,
                                                           promo.type,
                                                           promo.creator, promo.created_date, promo.description,
                                                           promo.value))

        email.html(email_html)

        try:
            email.send()
        except EmailErrors as e:
            raise FailedToSendEmail(e)

    @staticmethod
    def who_reserved(date, schedule, turn) -> list:
        """
        Finds the pilots in a particular reservation
        :param date: The date of the reservation to be found
        :param schedule: The schedule of the reservation to be found
        :param turn: The turn of the reservation to be found
        :return: The information of the pilots in the found reservation
        """
        for d in Database.find(DATES, {}):
            prob_date = Date(**d)
            if datetime.datetime.strftime(prob_date.date, "%Y-%m-%d") == date:
                for s in prob_date.schedules:
                    if s.hour == schedule:
                        for t in s.turns:
                            if t.turn_number == int(turn):
                                return t.pilots
        raise ReservationNotFound("La reservación con los parámetros dados no ha sido encontrada.")

    @staticmethod
    def get_party_avg_size() -> list:
        """
        Calculates the party average size taking into account every reservation
        :return: Party average size
        """
        expressions = list()
        expressions.append({"$match": {}})
        expressions.append({"$project": {
            "weekday": {"$dayOfWeek": "$date"},
            "schedules": "$schedules"
        }})
        expressions.append({"$unwind": "$schedules"})
        expressions.append({"$unwind": "$schedules.turns"})
        expressions.append({"$project": {
            "pilots_size": {"$size": "$schedules.turns.pilots"},
            "weekday": 1,
            "schedules": 1
        }})
        expressions.append({"$group": {
            "_id": {"weekday": "$weekday", "schedule": "$schedules.hour"},
            "party_size": {"$sum": "$pilots_size"}
        }})
        expressions.append({"$sort": {"_id.weekday": 1, "_id.schedule": 1}})
        result = list(Database.aggregate(DATES, expressions))
        return result

    @staticmethod
    def get_busy_hours() -> list:
        """
        Builds the occupation by hour and by week
        :return: The sum of the party size per hour and week
        """
        expressions = list()
        expressions.append({"$match": {}})
        expressions.append({"$project": {
            "weekday": {"$dayOfWeek": "$date"},
            "schedules": "$schedules"
        }})
        expressions.append({"$unwind": "$schedules"})
        expressions.append({"$unwind": "$schedules.turns"})
        expressions.append({"$project": {
            "pilots_size": {"$size": "$schedules.turns.pilots"},
            "weekday": 1,
            "schedules": 1
        }})
        expressions.append({"$group": {
            "_id": {"weekday": "$weekday", "schedule": "$schedules.hour"},
            "party_size": {"$sum": "$pilots_size"}
        }})
        expressions.append({"$sort": {"_id.weekday": 1, "_id.schedule": 1}})
        expressions.append({"$group": {
            "_id": {"schedule": "$_id.schedule"},
            "party_size": {"$sum": "$party_size"}
        }})
        expressions.append({"$sort": {"_id.schedule": 1}})
        result = list(Database.aggregate(DATES, expressions))
        return result

    @staticmethod
    def get_licensed_pilots(location: str) -> list:
        """
        Retrieves those pilots that have bought licenses
        :param location: Carso or Tlalnepantla
        :return: Licensed pilots information
        """
        expressions = list()
        expressions.append({"$match": {"location": {"$regex": location}}})
        result = list(Database.aggregate(PILOTS, expressions))
        return result

    @staticmethod
    def get_unprinted_licenses(location: str) -> list:
        """
        Retrieves those pilots whose license has not yet been produced
        :param location: Carso or Tlalnepantla
        :return: Licensed pilots information
        """
        expressions = list()
        first_date = datetime.datetime.now()
        expressions.append({'$match': {'date': {'$lte': first_date}}})
        expressions.append({"$unwind": "$pilots"})
        expressions.append({"$project": {"pilots": "$pilots"}})
        expressions.append({"$group": {
            "_id": {"email": "$pilots.email"}}})
        expressions.append({"$replaceRoot": {"newRoot": "$_id"}})
        emails = list(Database.aggregate('real_reservations', expressions))

        expressions = list()
        expressions.append({"$match": {"location": {"$regex": location}}})
        pilots = list(Database.aggregate('pilots', expressions))

        unprinted_licenses = list(filter(lambda pilot: pilot.get('email') not in [email.get('email')
                                                                                  for email in emails], pilots))
        return unprinted_licenses

    @staticmethod
    def change_license_status(location: str, pilot_id: str):
        """
        Updates the status of the pilot when their license has been printed
        :param pilot_id: ID of the pilot to be updated
        :param location: Carso or Tlalnepantla
        :return: Licensed pilot information
        """
        pilot = list(Database.find(PILOTS, {"_id": pilot_id}))
        if pilot is None or pilot == []:
            raise PilotNotFound("El piloto con el ID dado no existe")
        updated_pilot: Pilot = Pilot(**pilot[0])
        updated_pilot.licensed = False
        updated_pilot.update_mongo(PILOTS)
        return updated_pilot

    @staticmethod
    def get_reservations_income_qty(first_date, last_date) -> list:
        """
        Shows the amount earned in reservations and how many have been made in a given date range
        :param first_date: The start date to be accounted
        :param last_date: The end date to be accounted
        :return: The total income and quantity of all reservations
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({"$project": {"payment_total": "$payment.amount"}})
        expressions.append({"$group": {"_id": None, "income": {"$sum": "$payment_total"}, "qty": {"$sum": 1}}})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        return result

    @staticmethod
    def get_reservation_avg_price() -> list:
        """
        Calculates the reservation average size taking into account every reservation
        :return: Reservation average size
        """
        expressions = list()
        expressions.append({'$match': {}})
        expressions.append({"$project": {"payment_total": "$payment.amount"}})
        expressions.append({"$group": {"_id": None, "income": {"$sum": "$payment_total"}, "count": {"$sum": 1}}})
        expressions.append({"$project": {"avg_price": {"$divide": ["$income", "$count"]}}})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        return result

    @staticmethod
    def get_promos_discount_qty(first_date, last_date) -> list:
        """
        Shows the amount used in promos and how many have been accepted in a given date range
        :param first_date: The start date to be accounted
        :param last_date: The end date to be accounted
        :return: The total amount and quantity of all promos
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({"$match": {"discount": {"$ne": None}}})
        expressions.append({"$group": {"_id": None, "discount": {"$sum": "$discount"}, "qty": {"$sum": 1}}})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        return result

    @staticmethod
    def build_reservations_report(first_date, last_date) -> list:
        """
        Builds a report containing the information of the reservation: ID, Date, # of Pilots, # of Races, and total cost
        :param first_date: The start date to be accounted
        :param last_date: The end date to be accounted
        :return: A report with the reservations summary
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({"$sort": {"date": 1}})
        expressions.append({"$project": {"_id": 0,
                                         "ID_Reservación": "$_id",
                                         "Fecha": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                                         "Número_Pilotos": {"$size": "$pilots"},
                                         "Número_Carreras": {"$size": "$turns"},
                                         "Precio_Total": "$amount"}})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        if not result:
            raise ReportFailed("El reporte generó cero datos. Intente con otra fecha.")

        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        excel_path = f'{basedir}/app/reports/reservations/ReporteReservaciones_{date}.xlsx'
        return Utils.generate_report(result, f'ReporteReservaciones_{date}.xlsx', "Reservaciones")

    @staticmethod
    def build_pilots_report() -> list:
        """
        Builds a report containing the information of all pilots: Name, Last Name, Location, Birth Date,
                                                                  Postal Code, Nickname, City, # of reservation and # of
                                                                  careers made by that pilots, and total spent money
        :return: A report with the pilots summary
        """
        expressions = list()
        expressions.append({'$match': {}})
        expressions.append({"$addFields": {"pilots_size": {"$size": "$pilots"}}})
        expressions.append({"$unwind": "$pilots"})
        expressions.append({"$match": {"pilots.licensed": True}})
        expressions.append({"$project": {"turns": {"$size": "$turns"},
                                         "total_spent": {"$divide": ["$amount", "$pilots_size"]}, "pilots": "$pilots"}})
        expressions.append({"$group": {
            "_id": {"Nombre": "$pilots.name", "Apellido": "$pilots.last_name", "Email": "$pilots.email",
                    "Ubicación": "$pilots.location", "Fecha_Nacimiento": "$pilots.birth_date",
                    "Código_Postal": "$pilots.postal_code", "Nickname": "$pilots.nickname", "Ciudad": "$pilots.city"},
            "Número_Reservaciones": {"$sum": 1}, "Número_Carreras": {"$sum": "$turns"},
            "Total_Gastado": {"$sum": "$total_spent"}
        }})
        expressions.append({"$addFields": {"_id.Número_Reservaciones": "$Número_Reservaciones",
                                           "_id.Número_Carreras": "$Número_Carreras",
                                           "_id.Total_Gastado": "$Total_Gastado"}})
        expressions.append({"$replaceRoot": {"newRoot": "$_id"}})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        if not result:
            raise ReportFailed("El reporte generó cero datos. Intente con otra fecha.")

        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        excel_path = f'{basedir}/app/reports/pilots/ReportePilotos_{date}.xlsx'
        return Utils.generate_report(result, f'ReportePilotos_{date}.xlsx', "Pilotos")

    @classmethod
    def get_by_id(cls, _id, collection):
        """
        Retrieves the admin object with the given id, or raises an exception if that admin was not found
        :param _id: ID of the admin to find
        :param collection: Contains all the admins or super_admins
        :return: Admin object
        """
        admin = Database.find_one(collection, {'_id': _id})
        if admin:
            admin_obj: Admin = cls(**admin)
            return admin_obj
        else:
            admin = Database.find_one(SUPERADMINS, {'_id': _id})
            if admin:
                admin_obj: Admin = cls(**admin)
                return admin_obj
            raise AdminNotFound("El administrador con el ID dado no existe.")

    @staticmethod
    def block_turns(days: list, schedules: list, turns: list) -> None:
        print("kwargs", days, schedules, turns)
        days = [datetime.datetime.strptime(aware_datetime, "%Y-%m-%d").astimezone(get_localzone())
                for aware_datetime in days]
        print(days[0])
        dates = list(Database.find(DATES, {'date': {"$in": days}}))
        print(f"len de dates: {len(dates)}")
        for date in dates:
            updated_date = Date(**date)
            print(f"len de schedules {len(updated_date.schedules)}")
            for schedule in updated_date.schedules:
                if schedule.hour in schedules:
                    print("entro! en schedules")
                    for turn in schedule.turns:
                        if turn.turn_number in turns:
                            turn.type = "BLOQUEADO"
                            print(turn.type)
            updated_date.update_mongo(DATES)
