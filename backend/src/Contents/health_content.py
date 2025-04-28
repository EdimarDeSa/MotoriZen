from pydantic import Field

from Contents.base_content import BaseContent
from db.Models.health_model import HealthModel
from Utils.Internacionalization.text_handler import ModelsDescriptionTexts


class HealthContent(BaseContent):
    data: HealthModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
