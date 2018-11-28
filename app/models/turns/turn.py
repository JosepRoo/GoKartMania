import datetime

from flask import session
from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION, MEXICO_TZ
from app.models.dates.errors import DateNotAvailable
from app.models.reservations.constants import COLLECTION_TEMP, COLLECTION as REAL_RESERVATIONS
from app.models.reservations.reservation import Reservation
from app.models.schedules.errors import ScheduleNotAvailable
from app.models.schedules.schedule import Schedule
from app.models.dates.date import Date as DateModel
from app.models.turns.errors import TurnNotFound, TurnNotAvailable

"""
This is the turn model object which will be used to append new turns to both the reservation
and the schedule, depending the POST method.
"""


class Turn(BaseModel):
    def __init__(self, schedule, turn_number, positions, _id=None):
        super().__init__(_id)
        self.schedule = schedule
        self.turn_number = turn_number
        self.positions = positions

    @classmethod
    def add(cls, reservation: Reservation, new_turn):
        """
        Inserts a new turn to the given reservation
        :param reservation: Reservation object
        :param new_turn: Turn to be added to the reservation
        :return: A brand new turn object
        """
        allocation_date = new_turn.pop('date')
        turn: Turn = cls(**new_turn)
        session['reservation_date'] = allocation_date
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION_TEMP)
        return turn

    @staticmethod
    def get(turn_id):
        """
        Retrieves the information of the turn with the given id.
        :param turn_id: The id of the turn to be read from the reservation
        :return: The requested turn
        """
        turn = list(Database.find(REAL_RESERVATIONS, {'turns._id': turn_id}))
        if turn is None or turn == []:
            raise TurnNotFound("El turno con el ID dado no existe")
        return list(filter(lambda x: x.get('_id') == turn_id, turn[0].get('turns')))[0]

    @classmethod
    def check_and_add(cls, reservation: Reservation, new_turn):
        """
        Verifies that a turn can accept the given pilots and adds them to the Date Collection and the current reservation
        :param reservation: Reservation object
        :param new_turn: Turn information
        :return: None, or schedule/turn not available anymore message
        """
        available_schedules = DateModel.get_available_schedules_user(reservation, new_turn.get('date'))
        still_available = cls.check_turn_availability(available_schedules, new_turn)
        # Verifies that the turn is is still available
        if still_available:
            turn_positions = \
                list(filter(lambda schedule: schedule['schedule'] == new_turn.get('schedule'), available_schedules))[
                    0].get(
                    'turns')[int(new_turn.get('turn_number')) - 1].get('positions')
            user_positions = new_turn.get('positions')
            # Verifies that the positions selected are still available
            positions_available = cls.check_positions_availability(turn_positions, user_positions)
            if positions_available:
                allocation_date = new_turn.get('date')
                DateModel.update_temp(allocation_date, new_turn, reservation.type, True)
                if reservation.turns != [] and reservation.turns is not None and reservation.turns[0].turn_number == 0:
                    # Update the pre-existing turn by default
                    print("Aqui nunca deberia entrar.")
                    return cls.update(reservation, new_turn, reservation.turns[0]._id, True)
                else:
                    return cls.add(reservation, new_turn)
            else:
                raise ScheduleNotAvailable("Las posiciones que seleccionaste ya no se encuentran disponibles.")
        else:
            raise TurnNotAvailable("Este turno ya no se encuentra disponible.")

    @staticmethod
    def check_date_availability(available_dates, new_turn) -> dict:
        """
        Checks the status of the date contained in a turn
        :param available_dates: The status of the dates
        :param new_turn: Turn with its information, such as the date
        :return: Turn information
        """
        return available_dates.get('cupo')

    @staticmethod
    def check_schedule_availability(available_schedules, new_turn) -> int:
        """
        Verifies if a given schedule is available
        :param available_schedules: All schedules in a given date
        :param new_turn: Turn information, such as the schedule
        :return: 0 or 1, depending the status of the schedule
        """
        today = MEXICO_TZ.localize(datetime.datetime.now())
        if today.strftime("%Y-%m-%d") == new_turn.get('date'):
            if today.hour > int(new_turn.get('schedule')):
                raise ScheduleNotAvailable("El horario que seleccionaste no se encuentra disponible por el momento.")
        return list(filter(lambda x: x.get('schedule') == new_turn.get('schedule'), available_schedules))[0].get('cupo')

    @staticmethod
    def check_turn_availability(available_schedules, new_turn) -> int:
        """
        Verifies that a given turn is still available, taking into account other completed reservations
        :param available_schedules: The schedules and their status of a given date
        :param new_turn: The turn information, such as the turn number
        :return: True or False, depending on the turn status
        """
        for schedule in available_schedules:
            if schedule.get('schedule') == new_turn.get('schedule'):
                for turn in schedule.get('turns'):
                    if turn.get('turn') == int(new_turn.get('turn_number')):
                        return turn.get('status')
        return False

    @staticmethod
    def check_positions_availability(turn_positions, user_positions) -> bool:
        """
        Verifies if the positions selected by the user are still available
        :param turn_positions: Positions used by other users
        :param user_positions: Positions selected by the user
        :return: True or False, depending the positions availability
        """
        return True not in [turn_positions[int(position[-1]) - 1].get('status') == 0
                            for position in user_positions.keys()]

    @classmethod
    def check_and_update(cls, reservation: Reservation, updated_turn: dict, is_user: bool):
        """
        Updates the information from the turn with the given id.
        :param is_user: Indicates whether the operation is being held by the user or the administrator
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :return: All the turns of the current reservation, with updated data
        """
        for turn in reservation.turns:
            if turn._id == updated_turn.get('_id'):
                allocation_date = updated_turn.get('date')
                viable_update = cls.verify_update(reservation, updated_turn, turn)
                if viable_update:
                    DateModel.update_temp(allocation_date, updated_turn, reservation.type, is_user)
                    return cls.update(reservation, updated_turn, updated_turn.get('_id'), is_user)
        raise TurnNotFound("El turno con el ID dado no existe")

    @classmethod
    def delete(cls, reservation: Reservation, turn_id: str, date: str, is_user: bool) -> None:
        """
        Removes from the current reservation the given turn
        :param is_user: Indicates whether the operation is being held by the user or the administrator
        :param date: Date of the turn-reservation to be deleted
        :param reservation: Reservation object containing the array of turns
        :param turn_id: ID of the turn to be removed
        :return: None
        """
        for turn in reservation.turns:
            if turn._id == turn_id:
                first_date = MEXICO_TZ.localize(datetime.datetime.strptime(date, "%Y-%m-%d"))
                last_date = first_date
                query = {'date': {'$gte': first_date, '$lte': last_date}}
                cls.remove_turn_pilots(reservation, turn, query)
                reservation.turns.remove(turn)
                if is_user:
                    return reservation.update_mongo(COLLECTION_TEMP)
                else:
                    return reservation.update_mongo(REAL_RESERVATIONS)
        raise TurnNotFound("El turno con el ID dado no existe")

    @classmethod
    def get_blocked_turns(cls, date: str) -> dict:
        """
        Retrieves all those turns that were blocked in the given date
        :param date: The date to look for blocked turns
        :return: JSON with blocked schedules and turns
        """
        date = MEXICO_TZ.localize(datetime.datetime.strptime(date, "%Y-%m-%d"))
        query = {'date': date}
        result: dict = Database.find_one(COLLECTION, query)
        if result:
            date = DateModel(**result)
            blocked_turns = {"schedules": list(),
                             "turns": list()}
            for schedule in date.schedules:
                for turn in schedule.turns:
                    if turn.type is not None:
                        if "BLOQUEADO" in turn.type:
                            if turn.turn_number not in blocked_turns.get('turns'):
                                blocked_turns.get('turns').append(turn.turn_number)
                            if schedule.hour not in blocked_turns.get('schedules'):
                                blocked_turns.get('schedules').append(schedule.hour)
            return blocked_turns
        else:
            raise ScheduleNotAvailable("El día que seleccionaste no se encuentra disponible.")

    @classmethod
    def verify_update(cls, reservation: Reservation, updated_turn: dict, former_turn: 'Turn'):
        """
        Checks that updating the reservation is doable, given any possible changes in the collection
        :param reservation: Reservation object
        :param updated_turn: The new turn information
        :param former_turn: Previous turn object
        :return: True if the update was successful; error message otherwise
        """
        first_date = MEXICO_TZ.localize(datetime.datetime.strptime(updated_turn.get('date'), "%Y-%m-%d"))
        last_date = first_date
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        pilots = cls.remove_turn_pilots(reservation, former_turn, query)
        available_dates = DateModel.get_available_dates_user(reservation, updated_turn.get('date'), updated_turn.get('date'))
        if cls.check_date_availability(available_dates[0], updated_turn):
            available_schedules = DateModel.get_available_schedules_user(reservation, updated_turn.get('date'))
            if cls.check_schedule_availability(available_schedules, updated_turn):
                turn_positions = \
                    list(
                        filter(lambda sch: sch['schedule'] == updated_turn.get('schedule'), available_schedules))[
                        0].get(
                        'turns')[int(updated_turn.get('turn_number')) - 1].get('positions')
                user_positions = updated_turn.get('positions')
                # Verifies that the positions selected are still available
                positions_available = cls.check_positions_availability(turn_positions, user_positions)
                if positions_available:
                    return True
                else:
                    cls.rollback_update(reservation, query, former_turn, pilots)
                    raise ScheduleNotAvailable("Las posiciones que seleccionaste ya no se encuentran disponibles.")
            else:
                cls.rollback_update(reservation, query, former_turn, pilots)
                raise ScheduleNotAvailable("El horario que seleccionaste no se encuentra disponible por el momento.")
        else:
            cls.rollback_update(reservation, query, former_turn, pilots)
            raise DateNotAvailable("La fecha que seleccionaste no se encuentra disponible por el momento.")

    @staticmethod
    def remove_turn_pilots(reservation: Reservation, former_turn: 'Turn', query: dict):
        """
        Removes the pilots from the turn in the corresponding date-schedule
        :param reservation: Reservation object
        :param former_turn: Previous turn object
        :param query: The query that pymongo will process
        :return: Pilots of a turn
        """
        for date in Database.find(COLLECTION, query):
            new_date = DateModel(**date)
            for schedule in new_date.schedules:
                if schedule.hour == former_turn.schedule:
                    for turn in schedule.turns:
                        if turn.turn_number == int(former_turn.turn_number):
                            pilots = turn.pilots.copy()
                            for pilot in pilots:
                                if pilot._id in [pilot._id for pilot in reservation.pilots]:
                                    turn.pilots.remove(pilot)
                            if "BLOQUEADO" not in turn.type and (turn.pilots is None or turn.pilots == []):
                                turn.type = None
                            new_date.update_mongo(COLLECTION)
                            return pilots

    @classmethod
    def remove_allocation_dates(cls, reservation: Reservation, current_turn) -> None:
        """
        Removes from the Dates collection the field of "allocation date" if the transaction was completed
        :param reservation: Reservation object
        :param current_turn: Turn with its information, such as the turn number
        :return: None
        """
        first_date = reservation.date
        last_date = first_date

        query = {'date': {'$gte': first_date, '$lte': last_date}}
        result = list(Database.find(COLLECTION, query))
        print(first_date,last_date, query)
        new_date = DateModel(**result[0])
        for schedule in filter(lambda schedule: schedule.hour == current_turn.schedule, new_date.schedules):
            for turn in filter(lambda turn: turn.turn_number == int(current_turn.turn_number), schedule.turns):
                pilots = turn.pilots.copy()
                for pilot in filter(lambda pilot: pilot._id in [pilot._id for pilot in reservation.pilots],
                                    pilots):
                    pilot.allocation_date = None
        new_date.update_mongo(COLLECTION)

    @classmethod
    def update(cls, reservation: Reservation, updated_turn, turn_id, is_user: bool) -> 'Turn':
        """
        Updates the information from the turn with the given id..
        :param is_user: Indicates whether the operation is being held by the user or the administrator
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :param turn_id: the ID of the turn to be updated
        :return: The object turn with updated data
        """
        for turn in reservation.turns:
            if turn._id == turn_id:
                allocation_date = updated_turn.pop('date')
                new_turn = cls(**updated_turn)
                aware_datetime = MEXICO_TZ.localize(datetime.datetime.strptime(allocation_date, "%Y-%m-%d"))
                reservation.date = aware_datetime
                reservation.turns.remove(turn)
                reservation.turns.append(new_turn)
                if is_user:
                    reservation.update_mongo(COLLECTION_TEMP)
                else:
                    reservation.update_mongo(REAL_RESERVATIONS)
                return new_turn
        raise TurnNotFound("El piloto con el ID dado no existe")

    @staticmethod
    def rollback_update(reservation: Reservation, query, former_turn, pilots):
        for date in Database.find(COLLECTION, query):
            new_date = DateModel(**date)
            for schedule in new_date.schedules:
                if schedule.hour == former_turn.schedule:
                    for turn in schedule.turns:
                        if turn.turn_number == int(former_turn.turn_number):
                            for pilot in pilots:
                                turn.pilots.append(pilot)
                            if turn.type is None or turn.pilots is None or turn.pilots == []:
                                if "BLOQUEADO" not in turn.type:
                                    turn.type = reservation.type
                            new_date.update_mongo(COLLECTION)


class AbstractTurn(BaseModel):
    def __init__(self, turn_number, type=None, pilots=None, _id=None):
        from app.models.pilots.pilot import AbstractPilot
        super().__init__(_id)
        self.turn_number = turn_number
        self.type = type
        self.pilots = [AbstractPilot(**pilot) for pilot in pilots] if pilots is not None else list()

    @classmethod
    def add(cls, schedule: Schedule, new_turn):
        """
        Inserts a new turn to the given schedule
        :param schedule: Reservation object
        :param new_turn: Turn to be added to the schedule
        :return: A brand new turn object
        """
        turn: AbstractTurn = cls(**new_turn)
        schedule.turns.append(turn)
        return turn
