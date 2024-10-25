from typing import Sequence

from pydantic import BaseModel, InstanceOf


class BaseQueryResponseModel(BaseModel):
    total_results: int
    results: Sequence[InstanceOf[BaseModel]]
