from app.models.baseError import BaseError


class RecoveryErrors(BaseError):
    pass


class UnableToRecoverPassword(RecoveryErrors):
    pass
