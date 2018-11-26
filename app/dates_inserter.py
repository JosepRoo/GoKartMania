from app.models.dates.date import Date as DateModel
from app.common.database import Database

Database.initialize()

try:
    month = DateModel.insert_dates()
    print(f"Mes insertado con exito : {month}")
except Exception as e:
    print(e.__repr__())
