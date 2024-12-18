from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import CarModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarContent(BaseContent):
    data: CarModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
