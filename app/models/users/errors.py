from app.models.baseError import BaseError


class UserErrors(BaseError):
    pass

class InvalidLogin(UserErrors):
    pass