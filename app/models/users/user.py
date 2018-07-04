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

    def __init__(self, email, name, reservations=list(), _id=None):
        super().__init__(_id)
        self.email = email
        self.name = name
        self.reservations = reservations

    @classmethod
    def get_by_email(cls, email):
        """
        Attempts to find a user according to the given email
        :param email: The email to be found in the User Collection
        :return: Found User object
        """
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

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
            new_user = cls(**kwargs)
            new_user.reservations.append(session['reservation'])
            new_user.save_to_mongo(COLLECTION)
        else:
            new_user = cls(**kwargs, _id=user._id)
            new_user.reservations.append(session['reservation'])
            new_user.update_mongo(COLLECTION)
        return new_user

    def send_recovery_message(self, reservation: Reservation, qr_code):
        """
        Sends an email to the current user with the summary of the reservation (all turns)
        :param qr_code:
        :param reservation: Reservation object
        :return: POST method requesting an email to be sent to the user making the reservation
        """
        # email = Email(to=self.email, subject='Confirmación de reservación')
        email = Email(to='areyna@sitsolutions.org', subject='Confirmación de reservación', qr_code=qr_code)

        turns_detail = ""
        for turn in reservation.turns:
            turns_detail += "<p>" + turn.schedule + " hrs - Turno " + turn.turn_number + "\n</p>"
            for key in turn.positions:
                for pilot in reservation.pilots:
                    if pilot._id == turn.positions.get(key):
                        turns_detail += "<p>" + key + " " + pilot.name + "\n</p>"
            turns_detail += "\n"

        pilots_detail = ""
        for pilot in reservation.pilots:
            pilots_detail += "<p>Nombre: " + pilot.name + "\n</p>"
            if pilot.email is not None:
                pilots_detail += "<p>Email: " + pilot.email + "\n</p>"
            if pilot.licensed:
                pilots_detail += "<p>Licencia: Sí" + "\n</p>"
            else:
                pilots_detail += "<p>Licencia: No" + "\n</p>"
            pilots_detail += "\n"

        email.text("Estimado {}:\n"
                   "Gracias por usar el servicio de Reservaciones de GoKartMania.\n"
                   "A continuación se desglosan los datos de su compra:\n\n"
                   "Número de confirmación:\n"
                   "{}\n\n"
                   "Ubicación:\n"
                   "{}\n\n"
                   "Fecha:\n"
                   "{}\n\n"
                   "Detalle de los turnos:\n"
                   "{}\n"
                   "Pilotos:\n"
                   "{}\n"
                   "Total de la compra:\n"
                   "${}\n\n"
                   "Presenta en taquilla el código adjunto para comenzar tu carrera.\n\n"
                   "En sus marcas. Listos. ¡Fuera!".format(self.name, reservation._id,
                                                           reservation.location.name,
                                                           reservation.date.strftime("%Y-%m-%d"),
                                                           turns_detail, pilots_detail, reservation.payment.amount))
        email_str = "inicio\n"
        for i in pilots_detail:
            email_str += ""

        email.html("<html>"
                   "    <head>Tu reservación.</head>"
                   "    <body>"
                   "        <h1>Estimado {}:\n</h1>"
                   "        <p>Gracias por usar el servicio de Reservaciones de GoKartMania.\n</p>"
                   "        <p>A continuación se desglosan los datos de su compra:\n\n</p>"
                   "        <strong>Número de confirmación:\n</strong>"
                   "        <p>{}\n\n</p>"
                   "        <strong>Ubicación:\n</strong>"
                   "        <p>{}\n\n</p>"
                   "        <strong>Fecha:\n</strong>"
                   "        <p>{}\n\n</p>"
                   "        <strong>Detalle de los turnos:\n</strong>"
                   "        {}\n"
                   "        <strong>Pilotos:\n</strong>"
                   "        {}\n"
                   "        <strong>Total de la compra:\n</strong>"
                   "        <p>${}\n\n</p>"
                   "        <p>Presenta en taquilla el código adjunto para comenzar tu carrera.\n\n</p>"
                   "        <img src='data:image/png;base64, {}' alt='QR Code' />"
                   "        <p>En sus marcas. Listos. ¡Fuera!</p>"
                   "    </body>"
                   "</html>".format(self.name, reservation._id, reservation.location.name,
                                    reservation.date.strftime("%Y-%m-%d"), turns_detail, pilots_detail,
                                    reservation.payment.amount, qr_code))
        print(qr_code)

        try:
            email.send()
            return email
        except EmailErrors as e:
            raise FailedToSendEmail(e)
