from pydantic import Field

from Contents.base_content import BaseContent
from db.Models import VehicleQueryResponseModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarsContent(BaseContent):
    data: VehicleQueryResponseModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
