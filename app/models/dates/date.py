from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION
import datetime
from random import randint, choice
from app.models.reservations.reservation import Reservation
import calendar
from tzlocal import get_localzone

"""
This is the date model object which will be used to insert new available dates into the database, 
and extract information about the availability of specific dates and schedules.
"""


class Date(BaseModel):
    def __init__(self, date, schedules=list(), _id=None):
        from app.models.schedules.schedule import Schedule
        super().__init__(_id)
        self.date = date
        self.schedules = [Schedule(**schedule) for schedule in schedules] if schedules else schedules

    @classmethod
    def add(cls, new_date, day):
        """
        Builds and adds a new day to the Date Collection
        :param new_date: Dictionary containing the year and month of the date to be built
        :param day: The day to be added to complete de daytime format
        :return: A brand new datetime
        """
        from app.models.schedules.schedule import Schedule as ScheduleModel
        d = datetime.datetime(new_date.get('year'), new_date.get('month'), day, 21)
        new_day = cls(date=d, schedules=[])
        for i in range(11, 22):
            ScheduleModel.add(new_day, {'hour': f'{i}', 'turns': []})
        new_day.save_to_mongo(COLLECTION)
        return new_day

    @classmethod
    def get_dates_in_range(cls, first_date, last_date):
        """
        Shows the date objects in the given range
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates in range
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        dates = []
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            new_date.date = new_date.date.strftime("%Y-%m-%d")
            dates.append(new_date)
        return dates

    @classmethod
    def get_available_dates(cls, reservation: Reservation, first_date, last_date):
        """
        Shows the date objects in the given range with the status of availability
        :param reservation: Reservation object
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates in range with their status
        """
        availability = cls.build_availability_dict(reservation, first_date, last_date)
        return {date: availability[date]['cupo'] for date in availability}

    @classmethod
    def get_available_schedules(cls, reservation: Reservation, date):
        """
        Shows the schedule objects in the given date with the status of availability
        :param reservation: Reservation object
        :param date: The date to be processed
        :return: JSON object with schedules, turns, and positions in the specified date with their status
        """
        availability = cls.build_availability_dict(reservation, date, date)
        return availability[date]

    @classmethod
    def build_availability_dict(cls, reservation: Reservation, first_date, last_date):
        """
        Builds a dictionary that contains the status of availability for each day, schedule, turn, and position
        :param reservation: Reservation object
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates, schedules, turns, and positions in the specified range, with their status
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        total_pilots = len(reservation.pilots)
        availability_dict = {}
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            availability_dict[new_date.date.strftime("%Y-%m-%d")] = {}
            busy_schedules = 0
            empty_schedules = 0
            for schedule in new_date.schedules:
                availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour] = {}
                busy_turns = 0
                for turn in schedule.turns:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number] = {}
                    for k in range(8):
                        if k+1 in [pilot.position for pilot in turn.pilots]:
                            availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number][f'pos{k+1}'] = 0
                        else:
                            availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number][f'pos{k+1}'] = 1
                    if turn.type is None:
                        availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number]['cupo'] = 2
                        continue
                    if turn.type != reservation.type or total_pilots + len(turn.pilots) > 8:
                        availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number]['cupo'] = 0
                        busy_turns += 1
                    else:
                        availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour][turn.turn_number]['cupo'] = 1
                if busy_turns == 5:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 0
                    busy_schedules += 1
                elif busy_turns == 0:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 2
                    empty_schedules += 1
                else:
                    availability_dict[new_date.date.strftime("%Y-%m-%d")][schedule.hour]["cupo"] = 1
            if busy_schedules == 11:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 0
            if empty_schedules == 11:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 2
            else:
                availability_dict[new_date.date.strftime("%Y-%m-%d")]["cupo"] = 1
        return availability_dict

    @classmethod
    def auto_fill(cls, first_date, last_date):
        """
        Automatically fills all dates in the given range with random turns and pilots, for testing only
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: None
        """
        first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        from app.models.pilots.pilot import AbstractPilot
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            i = 0
            arr = []
            for schedule in new_date.schedules:
                for turn in schedule.turns:
                    for x in range(randint(1, 8)):
                        AbstractPilot.add(turn, {'position': x+1})
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

    @staticmethod
    def insert_dates():
        """
        Adds to the Date Collection a whole month
        :return: None
        """
        now = datetime.datetime.now().astimezone(get_localzone())
        month_dates = calendar.monthrange(now.year, now.month)[1]
        for i in range(month_dates):
            Date.add({'year': now.year, 'month': now.month}, i+1)
