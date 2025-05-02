from Contents.base_content import BaseContent
from db.Models import RegisterModel, RegisterQueryResponseModel, VehicleModel
from pydantic import BaseModel, Field
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterContent(BaseContent):
    data: RegisterModel | list[RegisterModel] = Field(description=ModelsDescriptionTexts.BASE_DATA)


class RegistersContent(BaseContent):
    data: RegisterQueryResponseModel = Field(description=ModelsDescriptionTexts.BASE_DATA)


class RegisterNewContentData(BaseModel):
    register_data: RegisterModel = Field(description=ModelsDescriptionTexts.REGISTER_DATE)
    vehicle_data: VehicleModel = Field(description=ModelsDescriptionTexts.VEHICLE_DATA)


class RegisterNewContent(BaseContent):
    data: RegisterNewContentData = Field(description=ModelsDescriptionTexts.BASE_DATA)
