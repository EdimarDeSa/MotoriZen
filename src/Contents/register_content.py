from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import CarModel, RegisterModel, RegisterQueryResponseModel
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterContent(BaseContent):
    data: RegisterModel | list[RegisterModel] = Field(description=ModelsDescriptionTexts.BASE_DATA)


class RegistersContent(BaseContent):
    data: RegisterQueryResponseModel = Field(description=ModelsDescriptionTexts.BASE_DATA)


class RegisterNewContent(BaseContent):
    register_data: RegisterModel = Field(description=ModelsDescriptionTexts.REGISTER_DATE)
    car_data: CarModel = Field(description=ModelsDescriptionTexts.CAR_DATA)
