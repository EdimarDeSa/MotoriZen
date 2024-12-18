from pydantic import Field

from DB.Models.base_metadata_model import BaseMetadataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class ReportResponseMetadataModel(BaseMetadataModel):
    total_cars: int = Field(description=ModelsDescriptionTexts.TOTAL_CARS)
    total_reports_selected: int = Field(description=ModelsDescriptionTexts.TOTAL_RESULTS)
