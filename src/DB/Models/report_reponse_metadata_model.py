from pydantic import BaseModel, Field


class ReportResponseMetadataModel(BaseModel):
    total_cars: int = Field(description="Total cars existent in the database for the given filter.")
    total_results: int = Field(description="Total results existent in the database for the given filter.")
    total_reports_selected: int = Field(description="Total reports selected.")
    total_bites: str = Field(description="Total bites selected.")
