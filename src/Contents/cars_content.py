from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import CarQueryResponseModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarsContent(BaseContent):
    data: CarQueryResponseModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
