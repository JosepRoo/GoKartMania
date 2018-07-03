from flask import session
from app import Database
from app.common.utils import Utils
from app.models.baseModel import BaseModel
from app.models.emails.email import Email
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
        new_user = cls(**kwargs)
        new_user.reservations.append(session['reservation'])
        if user is None:
            new_user.save_to_mongo(COLLECTION)
        else:
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
            turns_detail += turn.schedule + " hrs - Turno: " + turn.turn_number + "\n"
            for key in turn.positions:
                for pilot in reservation.pilots:
                    if pilot._id == turn.positions.get(key):
                        turns_detail += key + " " + pilot.name + "\n"
            turns_detail += "\n"

        pilots_detail = ""
        for pilot in reservation.pilots:
            pilots_detail += "Nombre: " + pilot.name + "\n"
            if pilot.email is not None:
                pilots_detail += "Email: " + pilot.email + "\n"
            if pilot.licensed:
                pilots_detail += "Licencia: Sí" + "\n"
            else:
                pilots_detail += "Licencia: No" + "\n"
            pilots_detail += "\n"

        email.text("Estimado {}:\n"
                   "Gracias por usar el servicio de Reservaciones de GoKartMania.\n"
                   "A continuación se desglosan los datos de su compra:\n"
                   "Número de confirmación:\n"
                   "{}\n"
                   "Ubicación:\n"
                   "{}\n"
                   "Fecha:\n"
                   "{}\n"
                   "Detalle de los turnos:\n"
                   "{}\n\n"
                   "Pilotos:\n"
                   "{}\n\n"
                   "Total de la compra:\n"
                   "${}\n\n"
                   "En sus marcas. Listos. ¡Fuera!".format(self.name, reservation._id,
                                                           reservation.location[0].name, reservation.date,
                                                           turns_detail, pilots_detail, reservation.payment[0].amount))
        email.html("<html></html>")
        email.send()
        return email

