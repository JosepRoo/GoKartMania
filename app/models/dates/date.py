from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION
import datetime
from random import randint, choice

from app.models.reservations.reservation import Reservation


class Date(BaseModel):
    def __init__(self, date, schedules=list(), _id=None):
        from app.models.schedules.schedule import Schedule
        super().__init__(_id)
        self.date = date
        self.schedules = [Schedule(**schedule) for schedule in schedules] if schedules else schedules

    @classmethod
    def add(cls, new_date, day):
        from app.models.schedules.schedule import Schedule as ScheduleModel
        d = datetime.datetime(new_date.get('year'), new_date.get('month'), day, 21)
        new_day = cls(date=d, schedules=[])
        for i in range(11, 22):
            ScheduleModel.add(new_day, {'hour': i, 'turns': []})
        new_day.save_to_mongo(COLLECTION)
        return new_day

    @classmethod
    def get_dates_in_range(cls, first_date, last_date):
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        print(first_date)
        print(last_date)
        dates = []
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            new_date.date = new_date.date.strftime("%Y-%m-%d")
            dates.append(new_date)
        return dates

    @classmethod
    def get_available_dates(cls, reservation: Reservation):
        total_pilots = len(reservation.pilots)
        availability_dict = {}
        for date in Database.find(COLLECTION, {}):
            new_date = cls(**date)
            availability_dict[new_date.date.strftime("%Y-%m-%d")] = {}
            availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 2
            busy_schedules = 0
            for schedule in new_date.schedules:
                availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour] = {}
                availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 2
                busy_turns = 0
                for turn in schedule.turns:
                    for pilot in turn.pilots:
                        availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number] = {}
                        availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number][pilot._id] = pilot.position
                    if turn.type is None:
                        continue
                    if turn.type != reservation.type or total_pilots + len(turn.pilots) > 8:
                        print("turno lleno")
                        busy_turns += 1
                if busy_turns == 5:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 0
                    print("hora llena")
                    busy_schedules += 1
                elif busy_turns == 0:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 2
                else:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 1
            if busy_schedules == 11:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 0
                print("día lleno")
            if busy_schedules == 0:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 2
            else:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 1
        return availability_dict

    @classmethod
    def auto_fill(cls):
        from app.models.pilots.pilot import AbstractPilot
        for date in Database.find(COLLECTION, {}):
            new_date = cls(**date)
            i = 0
            arr = []
            for schedule in new_date.schedules:
                for turn in schedule.turns:
                    # for x in range(randint(1, 8)):
                    #    AbstractPilot.add(turn, {'position': x+1})
                    if i == 0:
                        turn.type = choice(['Niño', 'Adulto'])
                    elif i == 1 and arr[0] == 'Niño':
                        turn.type = 'Adulto'
                    elif i == 1 and arr[0] == 'Adulto':
                        turn.type = choice(['Niño', 'Adulto'])
                    elif arr[-1] != 'Niño' and arr[-2] != 'Niño':
                        turn.type = choice(['Niño', 'Adulto'])
                    else:
                        turn.type = 'Adulto'
                    arr.append(turn.type)
                    i += 1
            print(arr)
            new_date.update_mongo(COLLECTION)
