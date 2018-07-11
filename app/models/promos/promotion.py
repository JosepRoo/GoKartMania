import datetime
import uuid

from flask import session
from tzlocal import get_localzone

from app.common.utils import Utils
from app.models.baseModel import BaseModel
from app.common.database import Database
from app.models.promos.constants import COLLECTION
from app.models.promos.errors import WrongPromotionType, PromotionNotFound, PromotionUsed, PromotionExpired, \
    PromotionUnauthorised, CouponNotFound
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

    @staticmethod
    def get_coupon_by_id(promo_id, coupon_id):
        promo = Database.find_one(COLLECTION, {'_id': promo_id})
        if promo is None:
            raise PromotionNotFound("La promoción con el ID dado no existe.")
        promotion = Promotion(**promo)
        for coupon in promotion.coupons:
            if coupon._id == coupon_id:
                return coupon
        raise CouponNotFound("El cupón con el ID dado no existe.")


class Promotion(BaseModel):
    def __init__(self, existence, start_date, end_date, type, value, creator=None, authoriser=None, authorised=False,
                 description=None, created_date=None, coupons=list(), _id=None):
        super().__init__(_id)
        self.existence = existence
        self.start_date = start_date
        self.end_date = end_date
        self.type = type
        self.authoriser = authoriser
        self.creator = creator
        self.authorised = authorised
        self.created_date = created_date if created_date else datetime.datetime.now().astimezone(get_localzone())
        self.description = description
        self.value = value
        self.coupons = [Coupons(**coupon) for coupon in coupons] if coupons else coupons

    @classmethod
    def add(cls, new_promo):
        """
        Adds a new promotion to the Promos Collection with the given specifications
        :param new_promo: JSON object with the promo information
        :return: Promotion object
        """
        from app.models.admins.admin import Admin as AdminModel

        if new_promo.get('type') != "Descuento" and new_promo.get('type') != "Carreras" \
                and new_promo.get('type') != "Reservación":
            raise WrongPromotionType(
                "Error en el tipo de promoción. Solo puede ser 'Descuento', 'Reservación' o 'Carreras'.")
        password = new_promo.pop('password')
        promo = cls(**new_promo, coupons=[])
        admin = AdminModel.get_by_id(session['admin_id'], ADMIN_COLLECTION)
        promo.creator = admin.name
        if password != Utils.generate_password():
            promo.authorised = False
        else:
            promo.authorised = True
        AdminModel.send_alert_message(promo)
        for i in range(promo.existence):
            Coupons.add(promo)
        promo.save_to_mongo(COLLECTION)

    @classmethod
    def update(cls, updated_promo, promo_id):
        """
        Updates the information of the promo with the given id.
        :param promo_id: The promotion ID to be found in the Promo collection
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

    @staticmethod
    def find_promotion(promo_id):
        """
        Searches in the Promo Collection for a specific coupon with the given ID
        :param promo_id: The ID of the coupon to be found
        :return: Dictionary with the promo object and the coupon document, or Promo error
        """
        for promo in Database.DATABASE['promos'].find({'type': {'$regex': promo_id[:4].title()}}):
            coupon = list(filter(lambda c: c['_id'] == promo_id, promo.get('coupons')))
            if coupon:
                authorised = promo.get('authorised')
                if authorised:
                    start_date = datetime.datetime.strptime(promo.get('start_date'), "%Y-%m-%d")
                    end_date = datetime.datetime.strptime(promo.get('end_date'), "%Y-%m-%d")
                    now = datetime.datetime.now()
                    if start_date <= now <= end_date:
                        if coupon[0].get('status'):
                            return {'promo': promo, 'coupon': coupon[0]}
                        else:
                            raise PromotionUsed("La promoción con el ID dado ya fue utilizada.")
                    else:
                        raise PromotionExpired("La promoción con el ID dado ya expiró.")
                else:
                    raise PromotionUnauthorised("La promoción con el ID dado no está autorizada.")
        raise PromotionNotFound("La promoción con el ID dado no existe.")
