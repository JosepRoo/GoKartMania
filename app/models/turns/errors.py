from app.models.baseError import BaseError


class TurnErrors(BaseError):
    pass


class TurnNotFound(TurnErrors):
    pass


class TurnNotAvailable(TurnErrors):
    pass
