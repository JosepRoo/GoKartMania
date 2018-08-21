from app.models.baseModel import BaseModel
from app.models.dates.date import Date

"""
This is the reservation schedule object which will be used to insert 5 turns and pilots
"""


class Schedule(BaseModel):
    def __init__(self, hour, turns=None, _id=None):
        from app.models.turns.turn import AbstractTurn
        super().__init__(_id)
        self.hour = hour
        self.turns = [AbstractTurn(**turn) for turn in turns] if turns is not None else list()

    @classmethod
    def add(cls, date: Date, new_schedule):
        """
        Builds a new schedule object and adds five turns to it
        :param date: Date object
        :param new_schedule: Schedule object with default information
        :return: Schedule object
        """
        from app.models.turns.turn import AbstractTurn as TurnModel
        schedule: Schedule = cls(**new_schedule)
        for i in range(5):
            TurnModel.add(schedule, {'turn_number': i+1})
        date.schedules.append(schedule)
        return schedule
