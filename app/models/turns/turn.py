import datetime
from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.dates.constants import COLLECTION
from app.models.dates.errors import DateNotAvailable
from app.models.reservations.constants import COLLECTION_TEMP
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
        print(allocation_date)
        turn = cls(**new_turn)
        reservation.date = datetime.datetime.strptime(allocation_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION_TEMP)
        return turn

    @staticmethod
    def get(reservation: Reservation, turn_id):
        """
        Retrieves the information of the turn with the given id.
        :param reservation: Reservation object
        :param turn_id: The id of the turn to be read from the reservation
        :return: The requested turn
        """
        for turn in reservation.turns:
            if turn._id == turn_id:
                return turn
        raise TurnNotFound("El turno con el ID dado no existe")

    @classmethod
    def check_and_add(cls, reservation: Reservation, new_turn):
        available_schedules = DateModel.get_available_schedules(reservation, new_turn.get('date'))
        still_available = cls.check_turn_availability(available_schedules, new_turn)
        print(still_available)
        if still_available:
            turn_positions = available_schedules[new_turn.get('schedule')].get(int(new_turn.get('turn_number')))
            user_positions = new_turn.get('positions')
            print(turn_positions)
            print(user_positions)
            positions_available = cls.check_positions_availability(turn_positions, user_positions)
            if positions_available:
                allocation_date = new_turn.get('date')
                print(allocation_date)
                print("Todo chido hasta aquí.")
                DateModel.update_temp(allocation_date, new_turn, reservation.type)
                if reservation.turns != [] and reservation.turns is not None and reservation.turns[0].turn_number == 0:
                    # Actualizar el turno que ya existía por default
                    return cls.update(reservation, new_turn, reservation.turns[0]._id)
                else:
                    return cls.add(reservation, new_turn)
                # Actualizar en la Collection de Dates el turno, schedule y pilotos
            else:
                raise ScheduleNotAvailable("Las posiciones que seleccionaste ya no se encuentran disponibles.")
        else:
            raise TurnNotAvailable("Este turno ya no se encuentra disponible.")

    @staticmethod
    def check_date_availability(available_dates, new_turn):
        return available_dates.get(new_turn.get('date'))

    @staticmethod
    def check_schedule_availability(available_schedules, new_turn):
        return available_schedules.get(new_turn.get('schedule')).get('cupo')

    @staticmethod
    def check_turn_availability(available_schedules, new_turn):
        return available_schedules.get(new_turn.get('schedule')).get(int(new_turn.get('turn_number'))).get('cupo')

    @staticmethod
    def check_positions_availability(turn_positions, user_positions):
        return True not in [turn_positions[position] == 0 for position in user_positions.keys()]

    @classmethod
    def check_and_update(cls, reservation: Reservation, updated_turn, turn_id):
        """
        Updates the information from the turn with the given id.
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :param turn_id: the ID of the turn to be updated
        :return: All the turns of the current reservation, with updated data
        """
        for turn in reservation.turns:
            if turn._id == turn_id:
                allocation_date = updated_turn.get('date')
                viable_update = cls.verify_update(reservation, updated_turn, turn)
                if viable_update:
                    DateModel.update_temp(allocation_date, updated_turn, reservation.type)
                    return cls.update(reservation, updated_turn, turn_id)
        raise TurnNotFound("El turno con el ID dado no existe")

    @classmethod
    def verify_update(cls, reservation: Reservation, updated_turn, former_turn):
        first_date = datetime.datetime.strptime(reservation.date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(reservation.date, "%Y-%m-%d") + datetime.timedelta(days=1)
        query = {'date': {'$gte': first_date, '$lte': last_date}}
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
                            if turn.pilots is None or turn.pilots == []:
                                turn.type = None
                            new_date.update_mongo(COLLECTION)
        available_dates = DateModel.get_available_dates(reservation, updated_turn.get('date'), updated_turn.get('date'))
        if cls.check_date_availability(available_dates, updated_turn):
            available_schedules = DateModel.get_available_schedules(reservation, updated_turn.get('date'))
            if cls.check_schedule_availability(available_schedules, updated_turn):
                return True
            else:
                raise ScheduleNotAvailable("El horario que seleccionaste no se encuentra disponible por el momento.")
        else:
            raise DateNotAvailable("La fecha que seleccionaste no se encuentra disponible por el momento.")

    @classmethod
    def remove_allocation_dates(cls, reservation: Reservation, current_turn):
        first_date = reservation.date
        last_date = reservation.date + datetime.timedelta(days=1)
        query = {'date': {'$gte': first_date, '$lte': last_date}}
        for date in Database.find(COLLECTION, query):
            new_date = DateModel(**date)
            for schedule in new_date.schedules:
                if schedule.hour == current_turn.schedule:
                    for turn in schedule.turns:
                        if turn.turn_number == int(current_turn.turn_number):
                            pilots = turn.pilots.copy()
                            for pilot in pilots:
                                if pilot._id in [pilot._id for pilot in reservation.pilots]:
                                    pilot.allocation_date = None
                            new_date.update_mongo(COLLECTION)

    @classmethod
    def update(cls, reservation: Reservation, updated_turn, turn_id):
        """
        Updates the information from the turn with the given id.
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :param turn_id: the ID of the turn to be updated
        :return: All the turns of the current reservation, with updated data
        """
        for turn in reservation.turns:
            if turn._id == turn_id:
                allocation_date = updated_turn.pop('date')
                new_turn = cls(**updated_turn, _id=turn_id)
                reservation.date = datetime.datetime.strptime(allocation_date, "%Y-%m-%d") + datetime.timedelta(days=1)
                reservation.turns.remove(turn)
                reservation.turns.append(new_turn)
                reservation.update_mongo(COLLECTION_TEMP)
                return reservation.turns
        raise TurnNotFound("El piloto con el ID dado no existe")


class AbstractTurn(BaseModel):
    def __init__(self, turn_number, type=None, pilots=list(), _id=None):
        from app.models.pilots.pilot import AbstractPilot
        super().__init__(_id)
        self.turn_number = turn_number
        self.type = type
        self.pilots = [AbstractPilot(**pilot) for pilot in pilots] if pilots else pilots

    @classmethod
    def add(cls, schedule: Schedule, new_turn):
        """
        Inserts a new turn to the given schedule
        :param schedule: Reservation object
        :param new_turn: Turn to be added to the schedule
        :return: A brand new turn object
        """
        turn = cls(**new_turn)
        schedule.turns.append(turn)
        return turn

