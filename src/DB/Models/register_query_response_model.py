from typing import Sequence

from pydantic import Field

from DB.Models import RegisterModel
from DB.Models.base_query_response_model import BaseQueryResponseModel


class RegisterQueryResponseModel(BaseQueryResponseModel):
    results: Sequence[RegisterModel] = Field(description="Results of the query.")