from app.models.baseModel import BaseModel
from app.models.pilots.errors import InvalidLogin
from app.models.users.user import User


class Pilot(BaseModel):
    def __init__(self, name, last_name, location, birth_date, postal_code, nickname, city, _id=None):
        super().__init__(_id)
        self.name = name
        self.lastName = last_name
        self.location = location
        self.birthDate = birth_date
        self.postalCode = postal_code
        self.nickname = nickname
        self.city = city
