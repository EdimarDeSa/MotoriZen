from pydantic import Field

from Contents.base_content import BaseContent
from db.Models import VehicleModel
from Utils.Internacionalization import ModelsDescriptionTexts


class VehicleContent(BaseContent):
    data: VehicleModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
