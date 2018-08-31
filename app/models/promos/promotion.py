import datetime
import uuid

from flask import session
from app.common.utils import Utils
from app.models.admins.errors import InvalidLogin
from app.models.baseModel import BaseModel
from app.common.database import Database
from app.models.dates.constants import MEXICO_TZ
from app.models.promos.constants import COLLECTION
from app.models.promos.errors import WrongPromotionType, PromotionNotFound, PromotionUsed, PromotionExpired, \
    PromotionUnauthorised, CouponNotFound
from app.models.admins.constants import COLLECTION as ADMIN_COLLECTION, SUPERADMINS

"""
This is the promotion model that will handle the request of the admin and user in their payments and creation
"""


class Coupons(BaseModel):
    def __init__(self, copies_left=None, date_applied=None, status=True, _id=None):
        super().__init__(_id)
        self.date_applied = date_applied
        self.status = status
        self.copies_left = copies_left

    @classmethod
    def add(cls, promo, copies_left: int, prefix: str) -> None:
        """
        Adds an empty default coupon to the given promotion
        :param prefix: The customisable prefix given by the admin
        :param copies_left: The number of copies of a coupon
        :param promo: The promotion Object
        :return: None
        """
        if prefix is not None:
            coupon: Coupons = cls(_id=prefix.lower() + "-" + promo.type[:4].lower() + "-" + uuid.uuid4().hex[:5],
                                  copies_left=copies_left)
        else:
            coupon: Coupons = cls(_id=promo.type[:4].lower()+"-"+uuid.uuid4().hex[:5], copies_left=copies_left)
        promo.coupons.append(coupon)

    @staticmethod
    def get_coupon_by_id(promo_id, coupon_id):
        """
        Retrieves a coupon given its ID
        :param promo_id: ID of the promotion
        :param coupon_id: ID of the coupon
        :return: Coupon information or error message if either promotion or coupon does not exist
        """
        promo = Database.find_one(COLLECTION, {'_id': promo_id})
        if promo is None:
            raise PromotionNotFound("La promoción con el ID dado no existe.")
        promotion = Promotion(**promo)
        for coupon in promotion.coupons:
            if coupon._id == coupon_id:
                return coupon
        raise CouponNotFound("El cupón con el ID dado no existe.")


class Promotion(BaseModel):
    def __init__(self, existence, start_date, end_date, required_races, at_least, type, value, creator=None,
                 authoriser=None, authorised=False, description=None, created_date=None, coupons=None, _id=None):
        super().__init__(_id)
        self.existence = existence
        self.start_date = start_date
        self.end_date = end_date
        self.required_races = required_races
        self.at_least = at_least
        self.type = type
        self.authoriser = authoriser
        self.creator = creator
        self.authorised = authorised
        self.created_date = created_date if created_date else datetime.datetime.now().astimezone(MEXICO_TZ)
        self.description = description
        self.value = value
        self.coupons = [Coupons(**coupon) for coupon in coupons] if coupons is not None else list()

    @classmethod
    def add(cls, new_promo: dict):
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
        copies_left: int = new_promo.pop('copies_left')
        prefix: str = new_promo.pop('prefix')

        promo: Promotion = cls(**new_promo, coupons=[])
        admin = AdminModel.get_by_id(session['admin_id'], ADMIN_COLLECTION)
        promo.creator = admin.name
        if password != Utils.generate_password():
            promo.authorised = False
        else:
            promo.authorised = True
        AdminModel.send_alert_message(promo)
        for i in range(promo.existence):
            Coupons.add(promo, copies_left, prefix)
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
            raise PromotionNotFound("La promo con el ID dado no existe.")
        updated_promo.pop('password')
        copies_left: int = updated_promo.pop('copies_left')
        prefix: str = updated_promo.pop('prefix')
        promo_obj: Promotion = cls(**updated_promo, _id=promo_id, coupons=promo.get('coupons'),
                                   creator=promo.get('creator'))
        #for coupon in promo_obj.coupons:
        #    coupon.copies_left = copies_left
        promo_obj.authoriser = "Admnistrador"
        promo_obj.update_mongo(COLLECTION)
        return promo_obj

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
    def find_promotion(promo_id) -> dict:
        """
        Searches in the Promo Collection for a specific coupon with the given ID
        :param promo_id: The ID of the coupon to be found
        :return: Dictionary with the promo object and the coupon document, or Promo error
        """
        for promo in Database.DATABASE['promos'].find({'type': {'$regex': promo_id[-10:-6].title()}}):
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
