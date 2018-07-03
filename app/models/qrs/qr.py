import qrcode

from app.models.baseModel import BaseModel
from app.models.emails.email import Email
from app.models.reservations.reservation import Reservation


class QR(BaseModel):
    def __init__(self, _id=None, url=None):
        super().__init__(_id)
        self.url = url

    @classmethod
    def create(cls, reservation: Reservation):
        """
        Creates a QR and saves an image of an instance in the `reservation_qrs` directory
        :param reservation: Reservation object
        :return: Path pointing to the location of the qr code image
        """
        qr = cls(**{})
        qr.url = f'/gokartmania.com/#/reservation/{reservation._id}'
        img = qrcode.make(qr.url)
        img_path = f'app/reservation_qrs/{qr._id}.png'
        img.save(img_path, format="PNG")
        # cls.send_confirmation_messages(img_path)
        return img_path

    # @staticmethod
    # def send_confirmation_messages(qr_code):
    #     """
    #     Sends an email to the given user with the instructions to change their password
    #     :return: POST method requesting an email to be sent to the user
    #     """
    #     email = Email(to="areyna@sitsolutions.org", subject='Confirmación de reservación')
    #     # email.text("Hola, {}:\nHas recibido este correo electrónico porque recientemente solicitaste restablecer "
    #     #                    "la contraseña asociada a tu cuenta de Iualia. Si no solicitaste este cambio, puedes hacer caso "
    #     #                    "omiso de este correo.\n\nCopia y pega el siguiente enlace en tu navegador de internet para restablecer tu contraseña:\n"
    #     #                    "iualia.com/user/reset_password/{}\n\nSaludos,\nEl equipo de Iualia .".format(self.name, recovery._id))
    #     email.text('This is a text body.')
    #     # email.html('<html><body>This is a text body.'
    #     #            '<div>'
    #     #            '    <img src="data:image/png;charset=utf-8;base64, {}"/>'
    #     #            '</div>'
    #     #            '</body></html>'.format(qr_code))
    #     print(qr_code)
    #     email.html(f'<html><body><div><img src="{qr_code}" /></div></body></html>')
    #     email.send()
    #     return email
