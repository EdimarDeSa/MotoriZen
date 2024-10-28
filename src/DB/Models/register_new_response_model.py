from pydantic import BaseModel, Field

from DB.Models.car_model import CarModel
from DB.Models.register_model import RegisterModel


class RegisterNewResponseModel(BaseModel):
    register_data: RegisterModel = Field(description="Register data inserted.")
    car_data: CarModel = Field(description="New car data after odometer update.")
