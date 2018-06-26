from app.models.baseModel import BaseModel
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
        turn = cls(**new_turn)
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
        if still_available:
            turn_positions = available_schedules[new_turn.get('schedule')].get(int(new_turn.get('turn_number')))
            user_positions = new_turn.get('positions')
            print(turn_positions)
            print(user_positions)
            positions__available = cls.check_positions_availability(turn_positions, user_positions)
            if positions__available:
                allocation_date = new_turn.pop('date')
                print(allocation_date)
                print("Todo chido hasta aquí.")
                if reservation.turns != [] and reservation.turns is not None and reservation.turns[0].turn_number == 0:
                    # Actualizar el turno que ya existía por default
                    cls.update(reservation, new_turn, reservation.turns[0]._id)
                else:
                    cls.add(reservation, new_turn)
                # Actualizar en la Collection de Dates el turno, schedule y pilotos
                DateModel.update_temp(allocation_date, new_turn, reservation.type)
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
    def update(cls, reservation: Reservation, updated_turn, turn_id):
        """
        Updates the information from the turn with the given id.
        :param reservation: Reservation object containing the array of turns
        :param updated_turn: The turn data to be updated to the previous one
        :param turn_id: the ID of the turn to be updated
        :return: All the turns of the current reservation, with updated data
        """
        # Modificar o agregar otro método para que compruebe que el Update sea viable
        # Si quiero cambiar de fecha, revisar que la fecha esté disponible con el cupo
        # Si quiero cambiar de horario, revisar que el horario esté disponible con el cupo
        # Si quiero cambiar de turno tengo que revisar que:
        # 1) El turno sea del mismo tipo que mi reservación
        # 2) Mi party quepa en ese nuevo turno
        # 3) Las posiciones que elegí estén disponibles, si no pedir nuevas posiciones
        viable_update = cls.verify_update(reservation, updated_turn, turn_id)
        if viable_update:
            for turn in reservation.turns:
                if turn._id == turn_id:
                    updated_turn.pop('date')
                    new_turn = cls(**updated_turn, _id=turn_id)
                    reservation.turns.remove(turn)
                    reservation.turns.append(new_turn)
                    reservation.update_mongo(COLLECTION_TEMP)
                    return reservation.turns
            raise TurnNotFound("El piloto con el ID dado no existe")
        else:
            pass

    @classmethod
    def verify_update(cls, reservation: Reservation, updated_turn, turn_id):
        # Método 1: "Borrar" temporalmente de la colección el piloto
        # Revisar si hay pilotos con una allocation_date nula
        # Si hay, entonces no setear el tipo a null, si era el único piloto
        # entonces setear el tipo del turno a null.
        # Construir el availability_dict tomando en cuenta este cambio y revisar si cabe en el nuevo dict
        # Si no cabe, entonces regresar el turno a donde estaba (?)
        # Si sí cabe, entonces ponerlo ahí.
        available_dates = DateModel.get_available_dates(reservation, updated_turn.get('date'), updated_turn.get('date'))
        if cls.check_date_availability(available_dates, updated_turn):
            available_schedules = DateModel.get_available_schedules(reservation, updated_turn.get('date'))
            if cls.check_schedule_availability(available_schedules, updated_turn):
                pass
            raise ScheduleNotAvailable("El horario que seleccionaste no se encuentra disponible por el momento.")
        raise DateNotAvailable("La fecha que seleccionaste no se encuentra disponible por el momento.")


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

