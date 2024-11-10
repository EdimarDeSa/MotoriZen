from pydantic import BaseModel, Field

from DB.Models.report_reponse_metadata_model import ReportResponseMetadataModel
from Utils.custom_primitive_types import DataFrameType


class ReportResponseModel(BaseModel):
    results: DataFrameType = Field(description="Results of the query.")
    metadata: ReportResponseMetadataModel = Field("Reports metadata.")
