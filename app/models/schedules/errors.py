from app.models.baseError import BaseError


class ScheduleErrors(BaseError):
    pass


class ScheduleNotFound(ScheduleErrors):
    pass


class ScheduleNotAvailable(ScheduleErrors):
    pass
