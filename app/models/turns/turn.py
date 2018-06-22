from app.models.baseModel import BaseModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.reservation import Reservation
from app.models.schedules.schedule import Schedule
from app.models.dates.date import Date as DateModel
from app.models.turns.errors import TurnNotFound, TurnErrors

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
        turn = cls(**new_turn)
        reservation.turns.append(turn)
        reservation.update_mongo(COLLECTION_TEMP)
        return new_turn

    @classmethod
    def check_and_add(cls, reservation: Reservation, new_turn):
        available_schedules = DateModel.get_available_schedules(reservation, new_turn.get('date'))
        still_available = cls.check_turn_availability(available_schedules, new_turn)
        if still_available:
            turn_positions = available_schedules[new_turn.get('schedule')].get(int(new_turn.get('turn_number')))
            user_positions = new_turn.get('positions')
            print(turn_positions)
            print(user_positions)
            positions__available = cls.check_positions_availability(turn_positions, user_positions)
            if positions__available:
                print("Todo chido hasta aquí.")
                # Actualizar el turno que ya existía por default
                if reservation.turns is None:
                    new_turn.pop('date')
                    cls.add(reservation, new_turn)
                else:
                    try:
                        new_turn.pop('date')
                        cls.update(reservation, new_turn, reservation.turns[0]._id)
                    except TurnErrors as e:
                        print("No creo que llegue aquí.")
                        raise TurnNotFound("El piloto con el ID dado no existe")
            else:
                print("Las posiciones que seleccionaste ya no se encuentran disponibles.")
        else:
            print("Este turno ya no se encuentra disponible.")
        return still_available

    @staticmethod
    def check_turn_availability(available_schedules, new_turn):
        return available_schedules.get(new_turn.get('schedule')).get(int(new_turn.get('turn_number'))).get('cupo')

    @staticmethod
    def check_positions_availability(turn_positions, user_positions):
        return True not in [turn_positions[position] == 0 for position in user_positions.keys()]

    @classmethod
    def update(cls, reservation: Reservation, updated_turn, turn_id):
        """
        Updates the information from the turn with the given id.
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :param turn_id: the ID of the turn to be updated
        :return: All the turns of the current reservation, with updated data
        """
        # Modificar o agregar otro método para que compruebe que el Update sea viable
        for turn in reservation.turns:
            if turn._id == turn_id:
                new_turn = cls(**updated_turn, _id=turn_id)
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

