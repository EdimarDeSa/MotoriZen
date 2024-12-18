from typing import Generic, Sequence

from pydantic import BaseModel, Field

from DB.Models.base_query_metadata_model import BaseQueryMetadataModel
from Utils.custom_primitive_types import T
from Utils.Internacionalization import ModelsDescriptionTexts


class BaseQueryResponseModel(BaseModel, Generic[T]):
    results: Sequence[T] = Field(description=ModelsDescriptionTexts.RESULTS)
    metadata: BaseQueryMetadataModel = Field(description=ModelsDescriptionTexts.METADATA)
