from app.models.baseError import BaseError


class AdminErrors(BaseError):
    pass


class AdminNotFound(AdminErrors):
    pass


class InvalidLogin(AdminErrors):
    pass


class InvalidEmail(AdminErrors):
    pass
