from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field, InstanceOf


class BaseQueryResponseModel(BaseModel):

    total_results: int = Field(description="Total results")
    results: Sequence[InstanceOf[BaseModel]] = Field(description="Results of the query.")
