from app.models.pilots.pilot import AbstractPilot
from app.models.reservations.reservation import Reservation as ReservationModel

from app.common.database import Database

Database.initialize()

AbstractPilot.remove_allocated_pilots()
ReservationModel.remove_temporal_reservations()
