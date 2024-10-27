from typing import Sequence

from pydantic import Field

from db.Models import CarModel
from db.Models.base_query_response_model import BaseQueryResponseModel


class CarQueryResponseModel(BaseQueryResponseModel):
    results: Sequence[CarModel] = Field(description="Results of the query.")
