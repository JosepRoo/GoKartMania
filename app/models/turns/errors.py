from app.models.baseError import BaseError


class TurnErrors(BaseError):
    pass


class InvalidLogin(TurnErrors):
    pass
