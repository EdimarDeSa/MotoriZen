from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import CarModel, RegisterModel, RegisterQueryResponseModel


class RegisterContent(BaseContent):
    data: RegisterModel | list[RegisterModel]


class RegistersContent(BaseContent):
    data: RegisterQueryResponseModel


class RegisterNewContent(BaseContent):
    register_data: RegisterModel = Field(description="Register data inserted.")
    car_data: CarModel = Field(description="New car data after odometer update.")
