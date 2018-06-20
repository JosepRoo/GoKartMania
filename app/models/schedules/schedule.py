from app.models.baseModel import BaseModel
from app.models.dates.date import Date


class Schedule(BaseModel):
    def __init__(self, hour, turns=list(), _id=None):
        from app.models.turns.turn import AbstractTurn
        super().__init__(_id)
        self.hour = hour
        self.turns = [AbstractTurn(**turn) for turn in turns] if turns else turns

    @classmethod
    def add(cls, date: Date, new_schedule):
        from app.models.turns.turn import AbstractTurn as TurnModel
        schedule = cls(**new_schedule)
        for i in range(5):
            TurnModel.add(schedule, {'turn_number': i+1})
        date.schedules.append(schedule)
        return schedule
