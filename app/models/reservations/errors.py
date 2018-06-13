from app.models.baseError import BaseError


class ReservationErrors(BaseError):
    pass


class InvalidLogin(ReservationErrors):
    pass
