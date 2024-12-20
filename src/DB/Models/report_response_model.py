from pydantic import BaseModel, Field

from DB.Models.report_reponse_metadata_model import ReportResponseMetadataModel
from Utils.custom_primitive_types import DataFrameType
from Utils.Internacionalization import ModelsDescriptionTexts


class ReportResponseModel(BaseModel):
    results: DataFrameType = Field(description=ModelsDescriptionTexts.RESULTS)
    metadata: ReportResponseMetadataModel = Field(description=ModelsDescriptionTexts.METADATA)
