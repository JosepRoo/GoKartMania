from app.models.baseError import BaseError


class PromotionErrors(BaseError):
    pass


class PromotionNotFound(PromotionErrors):
    pass


class WrongPromotionType(PromotionErrors):
    pass


class PromotionUsed(PromotionErrors):
    pass
