from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import FuelTypeModel
from Utils.Internacionalization import ModelsDescriptionTexts


class FuelTypeContent(BaseContent):
    data: list[FuelTypeModel] | FuelTypeModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
