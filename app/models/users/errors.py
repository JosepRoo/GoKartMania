from app.models.baseError import BaseError


class UserErrors(BaseError):
    pass


class UserNotFound(UserErrors):
    pass


class InvalidLogin(UserErrors):
    pass


class UserAlreadyRegisteredError(UserErrors):
    pass


class InvalidEmail(UserErrors):
    pass
