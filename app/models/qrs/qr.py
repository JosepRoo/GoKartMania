import datetime

import qrcode
import os

from app.models.baseModel import BaseModel
from app.models.reservations.reservation import Reservation
from config import basedir


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
        qr.url = f'gokartmania.com/#/reservation/{reservation._id}'
        img = qrcode.make(qr.url)
        date_str = reservation.date.strftime("%Y-%m-%d")
        img_path = f'{basedir}/app/reservation_qrs/{qr._id}{date_str}.png'
        img.save(img_path, format="PNG")
        return qr._id + ".png"

    @staticmethod
    def remove_reservation_qrs():
        folder = f'{basedir}/app/reservation_qrs'
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    qr_date = datetime.datetime.strptime(file_path[-14:-4], "%Y-%m-%d")
                    today = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
                    if today > qr_date:
                        os.unlink(file_path)
            except Exception as e:
                print(e)
