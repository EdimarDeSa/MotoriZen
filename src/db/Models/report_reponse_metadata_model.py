from pydantic import Field

from db.Models.base_metadata_model import BaseMetadataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class ReportResponseMetadataModel(BaseMetadataModel):
    total_vehicles: int = Field(description=ModelsDescriptionTexts.TOTAL_VEHICLES)
    total_reports_selected: int = Field(description=ModelsDescriptionTexts.TOTAL_RESULTS)
