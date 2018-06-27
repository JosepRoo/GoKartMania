from app.models.baseError import BaseError


class DateErrors(BaseError):
    pass


class DateNotFound(DateErrors):
    pass


class DateNotAvailable(DateErrors):
    pass
