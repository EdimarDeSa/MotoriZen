from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import BrandModel
from Utils.Internacionalization import ModelsDescriptionTexts


class BrandContent(BaseContent):
    data: list[BrandModel] | BrandModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
