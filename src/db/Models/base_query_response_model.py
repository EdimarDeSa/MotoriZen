from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field, InstanceOf


class BaseQueryResponseModel(BaseModel):
    __config__: ConfigDict = Field(description="New register model config")

    total_results: int = Field(description="Total results")
    results: Sequence[InstanceOf[BaseModel]] = Field(description="Results of the query.")
