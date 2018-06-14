from app.models.baseError import BaseError


class ReservationErrors(BaseError):
    pass


class ReservationNotFound(ReservationErrors):
    pass


class InvalidLogin(ReservationErrors):
    pass
