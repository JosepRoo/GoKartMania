from app.models.baseError import BaseError


class PromotionErrors(BaseError):
    pass


class PromotionNotFound(PromotionErrors):
    pass


class CouponNotFound(PromotionErrors):
    pass


class WrongPromotionType(PromotionErrors):
    pass


class PromotionUsed(PromotionErrors):
    pass


class PromotionUnauthorised(PromotionErrors):
    pass


class PromotionExpired(PromotionErrors):
    pass


