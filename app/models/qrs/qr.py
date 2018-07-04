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
        #if not os.path.exists("app/reservation_qrs"):
        #    os.makedirs('app/reservation_qrs')
        img_path = f'{basedir}/app/reservation_qrs/{qr._id}.png'
        #img_file = open(img_path,"w+")
        img.save(img_path, format="PNG")
        #img_file.close()
        return qr._id+".png"

    @staticmethod
    def remove_reservations_qrs():
        folder = 'app/reservation_qrs'
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                return os.listdir(folder)
            except Exception as e:
                print(e)
