import datetime
import os

from flask import session

from app import Database
from app.common.utils import Utils
from app.models.admins.errors import InvalidEmail, InvalidLogin, AdminNotFound
from app.models.baseModel import BaseModel
from app.models.admins.constants import COLLECTION, SUPERADMINS
from app.models.dates.constants import COLLECTION as DATES
from app.models.reservations.constants import COLLECTION as RESERVATIONS
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
        Attempts to find a user according to the given email
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
        if email[email.index('@') + 1:] != 'gokartmania.com.mx':
            raise InvalidEmail("Credenciales incorrectas")
        # Esta contraseña debería ser comparada con la que guardemos en la BD
        password = data.get('password')
        #
        # if Utils.check_hashed_password(password, new_admin.password):
        #     pass

        if password != os.environ.get('GKM_PB_KEY') and password != Utils.generate_password():
            raise InvalidLogin("Credenciales incorrectas")
        admin = Admin.get_by_email(email)
        if admin is None:
            new_admin: Admin = cls(**data)
            new_admin.password = Utils.hash_password(new_admin.password)
            if password == Utils.generate_password():
                session['sudo'] = new_admin._id
                new_admin.save_to_mongo(SUPERADMINS)
            else:
                new_admin.save_to_mongo(COLLECTION)
        else:
            new_admin: Admin = cls(**data, _id=admin._id)
            new_admin.password = Utils.hash_password(new_admin.password)
            if password == Utils.generate_password():
                session['sudo'] = new_admin._id
                new_admin.update_mongo(SUPERADMINS)
            else:
                new_admin.update_mongo(COLLECTION)
        session['admin_id'] = new_admin._id
        return new_admin

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
    def get_licensed_pilots() -> list:
        """
        Retrieves those pilots that have bought licenses
        :return: Licensed pilots information
        """
        expressions = list()
        expressions.append({"$match": {}})
        expressions.append({"$unwind": "$pilots"})
        expressions.append({"$match": {"pilots.licensed": True}})
        expressions.append({"$project": {"pilots": "$pilots"}})
        expressions.append({"$group": {
            "_id": {"name": "$pilots.name", "last_name": "$pilots.last_name"}
        }})
        result = list(Database.aggregate(RESERVATIONS, expressions))
        return result

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

