from typing import Sequence

from pydantic import Field

from db.Models import RegisterModel
from db.Models.base_query_response_model import BaseQueryResponseModel


class RegisterQueryResponseModel(BaseQueryResponseModel):
    results: Sequence[RegisterModel] = Field(description="Results of the query.")
