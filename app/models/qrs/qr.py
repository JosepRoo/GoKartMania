import qrcode

from app.models.baseModel import BaseModel
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
        return img_path