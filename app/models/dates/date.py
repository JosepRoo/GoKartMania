from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION
import datetime


class Date(BaseModel):
    def __init__(self, day, schedules=list(), _id=None):
        super().__init__(_id)
        self.day = day
        self.schedules = schedules

    @classmethod
    def add(cls, new_date, day):
        from app.models.schedules.schedule import Schedule as ScheduleModel
        d = datetime.datetime(new_date.get('year'), new_date.get('month'), day, 1)
        print(d)
        new_day = cls(day=d, schedules=[])
        for i in range(11, 22):
            ScheduleModel.add(new_day, {'hour': i, 'turns': []})
        new_day.save_to_mongo(COLLECTION)
        return new_day
