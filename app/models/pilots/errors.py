from app.models.baseError import BaseError


class PilotErrors(BaseError):
    pass


class InvalidLogin(PilotErrors):
    pass
