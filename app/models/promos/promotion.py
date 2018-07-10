import datetime
import uuid

from flask import session
from tzlocal import get_localzone

from app.models.baseModel import BaseModel
from app.common.database import Database
from app.models.promos.constants import COLLECTION
from app.models.promos.errors import WrongPromotionType, PromotionNotFound
from app.models.admins.admin import Admin as AdminModel
from app.models.admins.constants import COLLECTION as ADMIN_COLLECTION

"""
This is the promotion model
"""


class Coupons(BaseModel):
    def __init__(self, date_applied=None, status=True, _id=None):
        super().__init__(_id)
        self.date_applied = date_applied
        self.status = status

    @classmethod
    def add(cls, promo):
        """
        Adds an empty default coupon to the given promotion
        :param promo: The promotion Object
        :return: Promo with coupon added
        """
        coupon = cls(_id=promo.type[:4].lower()+"-"+uuid.uuid4().hex[:5])
        promo.coupons.append(coupon)


class Promotion(BaseModel):
    def __init__(self, existence, start_date, end_date, type, value, creator=None, authoriser=None, authorised=False,
                 description=None, coupons=list(), _id=None):
        super().__init__(_id)
        self.existence = existence
        self.start_date = start_date
        self.end_date = end_date
        self.type = type
        self.authoriser = authoriser
        self.creator = creator
        self.authorised = authorised
        self.created_date = datetime.datetime.now().astimezone(get_localzone())
        self.description = description
        self.value = value
        self.coupons = coupons

    @classmethod
    def add(cls, new_promo):
        """
        Adds a new promotion to the Promos Collection with the given specifications
        :param new_promo: JSON object with the promo information
        :return: Promotion object
        """
        if new_promo.get('type') != "Descuento" and new_promo.get('type') != "Carreras" \
                and new_promo.get('type') != "Reservación":
            raise WrongPromotionType(
                "Error en el tipo de promoción. Solo puede ser 'Descuento', 'Reservación' o 'Carreras'.")
        promo = cls(**new_promo)
        promo.authorised = True
        # admin = AdminModel.get_by_id(session['admin_id'], ADMIN_COLLECTION)
        #promo.creator = admin.name
        promo.creator = "Adrián"
        # Mandar correo al superadmin
        # Actualizar el campo promo.authorised si la contraseña no coincide
        # Mandar correo de que alguien hice un POST con contraseña iválida
        for i in range(promo.existence):
            Coupons.add(promo)
        promo.save_to_mongo(COLLECTION)

    @classmethod
    def update(cls, updated_promo, promo_id):
        """
        Updates the information of the promo with the given id.
        :param promo_id:  The promotion ID to be found in the Promo collection
        :param updated_promo: The promotion data to be updated to the previous one
        :return: Location object with updated data
        """
        promo = Database.find_one(COLLECTION, {'_id': promo_id})
        if promo is None:
            raise PromotionNotFound("La ubicación con el ID dado no existe.")
        promo = cls(**updated_promo, _id=promo_id)
        promo.update_mongo(COLLECTION)
        return promo

    @staticmethod
    def delete(promo_id):
        """
        Removes from the Promo Collection the promo with the given id.
        :param promo_id: The id of the promo to be deleted
        :return: The remaining promos of the collection
        """
        promo = Database.remove(COLLECTION, {"_id": promo_id})
        if promo is None:
            raise PromotionNotFound("La promoción con el ID dado no existe.")
        return promo

    @classmethod
    def get_promos(cls, _id=None):
        """
        Fetches a list of the all the Promotion objects in the corresponding collection
        :param _id: The specific ID of a particular promo object
        :return: List of Promo objects or one specific Promo object
        """
        if _id is None:
            return [cls(**promo) for promo in Database.find(COLLECTION, {})]
        else:
            promo = Database.find_one(COLLECTION, {'_id': _id})
            if promo is None:
                raise PromotionNotFound("La promoción con el ID dado no existe.")
            return [cls(**promo)]
