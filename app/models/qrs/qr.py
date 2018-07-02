import base64
from io import BytesIO

import qrcode

from app.models.baseModel import BaseModel
from app.models.emails.email import Email


class QR(BaseModel):
    def __init__(self, _id=None, url=None, qrcode=None):
        super().__init__(_id)
        self.url = url
        self.qrcode = qrcode

    @classmethod
    def create(cls, reservation_id):
        qr = cls(**{})
        # gokartmania.com/reservation/reservation._id
        qr.url = f'/gokartmania.com/user/reservation/{reservation_id}'
        img = qrcode.make(qr.url)
        buffered = BytesIO()
        img.save("imagen1.png", format="PNG")
        qr.qrcode = base64.b64encode(buffered.getvalue()).__str__()
        #cls.send_confirmation_message(qr.qrcode)
        return qr

    @staticmethod
    def send_confirmation_message(qr_code):
        """
        Sends an email to the given user with the instructions to change their password
        :return: POST method requesting an email to be sent to the user
        """
        email = Email(to="areyna@sitsolutions.org", subject='Confirmación de reservación')
        # email.text("Hola, {}:\nHas recibido este correo electrónico porque recientemente solicitaste restablecer "
        #                    "la contraseña asociada a tu cuenta de Iualia. Si no solicitaste este cambio, puedes hacer caso "
        #                    "omiso de este correo.\n\nCopia y pega el siguiente enlace en tu navegador de internet para restablecer tu contraseña:\n"
        #                    "iualia.com/user/reset_password/{}\n\nSaludos,\nEl equipo de Iualia.".format(self.name, recovery._id))
        email.text('This is a text body.')
        # email.html('<html><body>This is a text body.'
        #            '<div>'
        #            '    <img src="data:image/png;charset=utf-8;base64, {}"/>'
        #            '</div>'
        #            '</body></html>'.format(qr_code))
        email.html('<html><body><div><img src="data:image/png;http://worldartsme.com/images/clip-art-red-dot-clipart-1.jpg" alt="Red dot2" /></div></body></html>')
        email.send()
        return email
