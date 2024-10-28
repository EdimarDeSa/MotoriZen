from typing import Sequence

from pydantic import Field

from DB.Models import CarModel
from DB.Models.base_query_response_model import BaseQueryResponseModel


class CarQueryResponseModel(BaseQueryResponseModel):
    results: Sequence[CarModel] = Field(description="Results of the query.")
