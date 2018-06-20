from app.models.baseError import BaseError


class PilotErrors(BaseError):
    pass


class PilotNotFound(PilotErrors):
    pass


class InvalidLogin(PilotErrors):
    pass
