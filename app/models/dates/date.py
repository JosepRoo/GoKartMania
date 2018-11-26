from flask import session

from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION, MEXICO_TZ
import datetime
from random import randint, choice

from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation
import calendar

"""
This is the date model object which will be used to insert new available dates into the database, 
and extract information about the availability of specific dates and schedules.
"""


class Date(BaseModel):
    def __init__(self, date, schedules=None, _id=None):
        from app.models.schedules.schedule import Schedule
        super().__init__(_id)
        self.date = date
        self.schedules = [Schedule(**schedule) for schedule in schedules] if schedules is not None else list()

    @classmethod
    def add(cls, new_date, day):
        """
        Builds and adds a new day to the Date Collection
        :param new_date: Dictionary containing the year and month of the date to be built
        :param day: The day to be added to complete de daytime format
        :return: A brand new datetime
        """
        from app.models.schedules.schedule import Schedule as ScheduleModel
        aware_datetime = MEXICO_TZ.localize(datetime.datetime(new_date.get('year'), new_date.get('month'), day))
        new_day: Date = cls(date=aware_datetime, schedules=[])
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
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(first_date, "%Y-%m-%d"))
        last_date = MEXICO_TZ.localize(datetime.datetime.strptime(last_date, "%Y-%m-%d"))
        dates = []
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        for date in Database.find(COLLECTION, query):
            new_date: Date = cls(**date)
            new_date.date = new_date.date.strftime("%Y-%m-%d")
            dates.append(new_date)
        return dates

    @classmethod
    def get_available_dates_user(cls, reservation: Reservation, first_date, last_date):
        """
        Shows the date objects in the given range with the status of availability
        :param reservation: Reservation object
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates in range with their status
        """
        availability = cls.build_availability_dict(reservation, first_date, last_date)
        available_dates = []
        for date in availability:
            available_dates.append({"fecha": date, "cupo": availability[date]['cupo']})
        return available_dates

    @classmethod
    def get_available_dates_admin(cls, first_date, last_date) -> list:
        """
        Shows the date objects in the given range with the status of availability
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates in range with their status
        """
        dates_status = cls.build_dates_status(first_date, last_date)
        return [{'date': date['date'], 'status': date['status']} for date in dates_status]

    @classmethod
    def get_available_schedules_user(cls, reservation: Reservation, date):
        """
        Shows the schedule objects in the given date with the status of availability
        :param reservation: Reservation object
        :param date: The date to be processed
        :return: JSON object with schedules, turns, and positions in the specified date with their status
        """
        availability = cls.build_availability_dict(reservation, date, date)
        availability_arr = []
        for date in availability:
            availability[date].pop('cupo')
            today = MEXICO_TZ.localize(datetime.datetime.now())
            reservation_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            for schedule in availability[date]:
                if today.strftime("%Y-%m-%d") == reservation_date.strftime("%Y-%m-%d"):
                    if int(schedule) > today.hour:
                        availability_arr.append(cls.fill_availability_arr(reservation, availability, date, schedule))
                elif reservation_date.strftime("%Y-%m-%d") > today.strftime("%Y-%m-%d"):
                    availability_arr.append(cls.fill_availability_arr(reservation, availability, date, schedule))
        return availability_arr

    @staticmethod
    def fill_availability_arr(reservation: Reservation, availability, date, schedule) -> dict:
        """
        Builds a schedule dictionary containing the status of the schedule, the turn and the positions
        :param reservation: Reservation object containing the schedules and turns
        :param availability: The dictionary of availability of all dates
        :param date: A given date by the user
        :param schedule: A given schedule by the user
        :return: A dictionary with schedules, status, and turns
        """
        schedule_turn = [(turn.schedule, turn.turn_number) for turn in reservation.turns]
        turns = []
        schedule_status = availability[date][schedule].pop('cupo')
        for turn in availability[date][schedule]:
            turn_status = availability[date][schedule][turn].pop('cupo')
            turns.append({"turn": turn, "status": turn_status,
                          "positions": [
                              {"position": position[-1], "status": availability[date][schedule][turn][position]}
                              for position in availability[date][schedule][turn]]})

        for i in range(len(turns)):
            result = list(filter(lambda x: schedule in x, schedule_turn))
            if result:
                turn = int(result[0][1])
                # Block the turn before and the turn after, for this user
                if (i - 1 == turn - 1) or (i + 1 == turn - 1):
                    turns[i]['status'] = 0
        schedule = {'schedule': schedule, 'cupo': schedule_status, 'turns': turns}
        return schedule

    @classmethod
    def get_available_schedules_admin(cls, date) -> list:
        """
        Shows the schedule objects in the given date with the status of availability
        :param date: The date to be processed
        :return: JSON object with schedules, turns, and positions in the specified date with their status
        """
        dates_status = cls.build_dates_status(date, date)
        return [{'schedules': date['schedules']} for date in dates_status]

    @classmethod
    def build_availability_dict(cls, reservation: Reservation, first_date, last_date) -> dict:
        """
        Builds a dictionary that contains the status of availability for each day, schedule, turn, and position
        :param reservation: Reservation object
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates, schedules, turns, and positions in the specified range, with their status
        """
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(first_date, "%Y-%m-%d"))
        last_date = MEXICO_TZ.localize(datetime.datetime.strptime(last_date, "%Y-%m-%d"))
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        total_pilots = len(reservation.pilots)
        availability_dict = {}

        # Builds an array containing only the types of the Dates in the given range
        expressions = list()
        expressions.append({'$match': {'date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({'$unwind': '$schedules'})
        expressions.append({'$unwind': '$schedules.turns'})
        expressions.append({'$replaceRoot': {'newRoot': "$schedules.turns"}})
        expressions.append({'$project': {'type': 1, '_id': 0}})
        result = list(Database.aggregate(COLLECTION, expressions))
        turn_types = [item.get('type') for item in result]

        i = 0
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            date_str = new_date.date.strftime("%Y-%m-%d")
            availability_dict[date_str] = {}
            busy_schedules = 0
            empty_schedules = 0
            # Counts how many days, schedules, and turns are occupied
            # 0 - Completely occupied
            # 1 - Moderately occupied
            # 2 - Completely empty
            for schedule in new_date.schedules:
                availability_dict[date_str][schedule.hour] = {}
                busy_turns = 0
                for turn in schedule.turns:
                    availability_dict[date_str][schedule.hour][turn.turn_number] = {}
                    for k in range(1, 9):
                        # Looks for any pre-occupied positions by other pilots
                        if k in [pilot.position for pilot in turn.pilots]:
                            availability_dict[date_str][schedule.hour][turn.turn_number][f'pos{k}'] = 0
                        else:
                            availability_dict[date_str][schedule.hour][turn.turn_number][f'pos{k}'] = 1
                    # Checks that there are at least two turns of Adults or None between Kids reservation
                    if turn.type is None:
                        f = lambda x: 0 if x < 0 else x
                        if "Niños" in turn_types[f(i - 2): i] + turn_types[i + 1: i + 3]:
                            availability_dict[date_str][schedule.hour][turn.turn_number]['cupo'] = 0
                            busy_turns += 1
                        else:
                            availability_dict[date_str][schedule.hour][turn.turn_number]['cupo'] = 2
                    elif "BLOQUEADO" in turn.type:
                        availability_dict[date_str][schedule.hour][turn.turn_number]['cupo'] = 0
                        busy_turns += 1
                    # Ensures that the type of the reservation matches the turn selected
                    # and that the party size fits in that turn
                    elif turn.type != reservation.type or total_pilots + len(turn.pilots) > 8:
                        availability_dict[date_str][schedule.hour][turn.turn_number]['cupo'] = 0
                        busy_turns += 1
                    else:
                        availability_dict[date_str][schedule.hour][turn.turn_number]['cupo'] = 1
                        busy_turns += 1
                    i += 1
                if busy_turns == 5:
                    availability_dict[date_str][schedule.hour]["cupo"] = 0
                    busy_schedules += 1
                elif busy_turns == 0:
                    availability_dict[date_str][schedule.hour]["cupo"] = 2
                    empty_schedules += 1
                else:
                    availability_dict[date_str][schedule.hour]["cupo"] = 1
            if busy_schedules == 11:
                availability_dict[date_str]["cupo"] = 0
            elif empty_schedules == 11:
                availability_dict[date_str]["cupo"] = 2
            else:
                availability_dict[date_str]["cupo"] = 1
        return availability_dict

    @classmethod
    def build_dates_status(cls, first_date, last_date) -> list:
        """
        Builds a dictionary that contains the status of availability for each day, schedule, turn, and position
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: JSON object with dates, schedules, turns, and positions in the specified range, with their status
        """
        dates = [date.json() for date in cls.get_dates_in_range(first_date, last_date)]
        dates_status = []
        for date in dates:
            schedules = []
            for schedule in date['schedules']:
                turns = []
                for turn in schedule['turns']:
                    if turn['type'] is None:
                        turn_status = 2
                    else:
                        if 'BLOQUEADO' in turn['type'] or len(turn['pilots']) == 8:
                            turn_status = 0
                        else:
                            turn_status = 1
                    positions = []
                    for k in range(1, 9):
                        # Looks for any pre-occupied positions by other pilots
                        if k in [pilot['position'] for pilot in turn['pilots']]:
                            position_status = 0
                        else:
                            position_status = 1
                        positions.append({"position": k, "status": position_status})
                    turns.append({"turn": turn['turn_number'], "type": turn['type'],
                                  "status": turn_status, "positions": positions})
                # Counts how many schedules are occupied
                # 0 - Completely occupied
                # 1 - Moderately occupied
                # 2 - Completely empty
                if len(list(filter(lambda race: race['status'] == 0, turns))) == 5:
                    schedule_status = 0
                elif len(list(filter(lambda race: race['status'] == 2, turns))) == 5:
                    schedule_status = 2
                else:
                    schedule_status = 1
                schedules.append({'schedule': schedule['hour'], 'status': schedule_status, 'turns': turns})
            if len(list(filter(lambda day: day['status'] == 0, schedules))) == 11:
                date_status = 0
            elif len(list(filter(lambda day: day['status'] == 2, schedules))) == 11:
                date_status = 2
            else:
                date_status = 1
            dates_status.append({'date': date['date'], 'status': date_status, 'schedules': schedules})
        return dates_status

    @classmethod
    def auto_fill(cls, first_date, last_date) -> None:
        """
        Automatically fills all dates in the given range with random turns and pilots, for testing only
        :param first_date: The start date in range
        :param last_date: The end date in range
        :return: None
        """
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(first_date, "%Y-%m-%d"))
        last_date = MEXICO_TZ.localize(datetime.datetime.strptime(last_date, "%Y-%m-%d"))
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        from app.models.pilots.pilot import AbstractPilot
        for date in Database.find(COLLECTION, query):
            new_date = cls(**date)
            i = 0
            arr = []
            for schedule in new_date.schedules:
                for turn in schedule.turns:
                    # Checks that there are at least two turns of Adults or None between Kids reservation
                    for x in range(randint(1, 8)):
                        AbstractPilot.add(turn, {'position': x + 1, 'allocation_date': None})
                    if i == 0:
                        turn.type = choice(['Niños', 'Adultos'])
                    elif i == 1 and arr[0] == 'Niños':
                        turn.type = 'Adultos'
                    elif i == 1 and arr[0] == 'Adultos':
                        turn.type = choice(['Niños', 'Adultos'])
                    elif arr[-1] != 'Niños' and arr[-2] != 'Niños':
                        turn.type = choice(['Niños', 'Adultos'])
                    else:
                        turn.type = 'Adultos'
                    arr.append(turn.type)
                    i += 1
            # print(arr)
            new_date.update_mongo(COLLECTION)

    @classmethod
    def update_temp(cls, allocation_date, new_turn, reservation_type, is_user: bool) -> None:
        """
        Updates the indicated date with the schedule, turn, type, pilots, and allocation date
        :param is_user: Indicates whether the operation is being held by the user or the administrator
        :param reservation_type: The type of reservation (Kids or Adults)
        :param allocation_date: The momentary date when the reservation will be occupied
        :param new_turn: The information of the turn
        :return: None
        """
        from app.models.pilots.pilot import AbstractPilot
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(allocation_date, "%Y-%m-%d"))
        last_date = MEXICO_TZ.localize(datetime.datetime.strptime(allocation_date, "%Y-%m-%d"))
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        updated_date = cls(**Database.find(COLLECTION, query)[0])
        for schedule in updated_date.schedules:
            if schedule.hour == new_turn.get('schedule'):
                turn_number = int(new_turn.get('turn_number'))
                for position in new_turn.get('positions'):
                    position_num = (int(position[-1]))
                    now = datetime.datetime.now(MEXICO_TZ)
                    if is_user:
                        AbstractPilot.add(schedule.turns[turn_number - 1],
                                          {'_id': new_turn.get('positions').get(position),
                                           'position': position_num,
                                           'allocation_date': now})
                    else:  # is_admin
                        AbstractPilot.add(schedule.turns[turn_number - 1],
                                          {'_id': new_turn.get('positions').get(position),
                                           'position': position_num,
                                           'allocation_date': None})
                # Update the type of turn, if it's None
                if schedule.turns[turn_number - 1].type is None:
                    schedule.turns[turn_number - 1].type = reservation_type
                updated_date.update_mongo(COLLECTION)

    @staticmethod
    def insert_dates() -> None:
        """
        Adds to the Date Collection a whole month, taking into account the last month in the collection
        :return: None
        """
        expressions = list()
        expressions.append({"$group": {"_id": None, "maxDate": {"$max": "$date"}}})
        result = list(Database.aggregate(COLLECTION, expressions))
        now = result[0].get('maxDate') + datetime.timedelta(days=1)
        month_dates = calendar.monthrange(now.year, now.month)[1]
        for i in range(month_dates):
            Date.add({'year': now.year, 'month': now.month}, i + 1)

