from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION
from app.models.pilots.pilot import Pilot
import datetime
from random import randint, choice


class Date(BaseModel):
    def __init__(self, day, schedules=list(), _id=None):
        from app.models.schedules.schedule import Schedule
        super().__init__(_id)
        self.day = day
        self.schedules = [Schedule(**schedule) for schedule in schedules] if schedules else schedules

    @classmethod
    def add(cls, new_date, day):
        from app.models.schedules.schedule import Schedule as ScheduleModel
        d = datetime.datetime(new_date.get('year'), new_date.get('month'), day, 21)
        new_day = cls(day=d, schedules=[])
        for i in range(11, 22):
            ScheduleModel.add(new_day, {'hour': i, 'turns': []})
        new_day.save_to_mongo(COLLECTION)
        return new_day

    @classmethod
    def get_all_dates(cls):
        dates = []
        for date in Database.find(COLLECTION, {}):
            new_date = cls(**date)
            new_date.day = new_date.day.strftime("%Y-%m-%d")
            dates.append(new_date)
        return dates

    @classmethod
    def auto_fill(cls):
        for date in Database.find(COLLECTION, {}):
            new_date = cls(**date)
            for schedule in new_date.schedules:
                for i in range(len(schedule.turns)):
                    #pilots = [Pilot('Juan') for x in range(randint(1, 8))]
                    #turn.pilots.append(pilots)
                    mode = choice(['Niño', 'Adulto'])
                    schedule.turns[i].type = mode
            new_date.update_mongo(COLLECTION)
