from app.models.baseError import BaseError


class EmailErrors(BaseError):
    pass


class FailedToSendEmail(EmailErrors):
    pass
