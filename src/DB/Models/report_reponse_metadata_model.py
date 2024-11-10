from pydantic import Field

from DB.Models.base_metadata_model import BaseMetadataModel


class ReportResponseMetadataModel(BaseMetadataModel):
    total_cars: int = Field(description="Total cars existent in the database for the given filter.")
    total_reports_selected: int = Field(description="Total reports selected.")
