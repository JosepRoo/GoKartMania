from app.models.baseError import BaseError


class LocationErrors(BaseError):
    pass


class LocationNotFound(LocationErrors):
    pass
