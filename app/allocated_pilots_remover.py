from app.models.pilots.pilot import AbstractPilot
from app.common.database import Database

Database.initialize()

AbstractPilot.remove_allocated_pilots()
