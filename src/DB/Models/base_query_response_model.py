from typing import Generic, Sequence

from pydantic import BaseModel, Field

from DB.Models.base_query_metadata_model import BaseQueryMetadataModel
from Utils.custom_primitive_types import T


class BaseQueryResponseModel(BaseModel, Generic[T]):
    results: Sequence[T] = Field(description="Results of the query.")
    metadata: BaseQueryMetadataModel = Field(description="Query metada.")
