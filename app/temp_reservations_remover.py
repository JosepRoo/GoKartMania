from app.models.reservations.reservation import Reservation as ReservationModel
from app.common.database import Database

Database.initialize()

ReservationModel.remove_temporal_reservations()
