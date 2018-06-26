from app.models.dates.date import Date as DateModel
from app.common.database import Database

Database.initialize()

DateModel.insert_dates()
