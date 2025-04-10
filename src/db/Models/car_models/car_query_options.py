from pydantic import field_validator

from db.Models.base_query_options_models import BaseQueryOptionsModel
from db.Schemas import CarSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError


class CarQueryOptionsModel(BaseQueryOptionsModel):
    @field_validator("sort_by", mode="after")
    def validate_sort_by(cls, value: str) -> str:
        if value is None:
            return "id_car"

        valid_sort_fields = CarSchema.fields()
        if value not in valid_sort_fields:
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_SORT_KEY,
                detail=f"Invalid sort_by key {value}. Valid keys: {', '.join(valid_sort_fields)}",
            ).as_http_response()
        return value
