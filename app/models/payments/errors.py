from app.models.baseError import BaseError


class PaymentErrors(BaseError):
    pass


class TokenisationFailed(PaymentErrors):
    pass


class PaymentFailed(PaymentErrors):
    pass
