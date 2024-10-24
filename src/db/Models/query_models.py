from typing import Optional

from pydantic import BaseModel, Field, field_validator

from db.Schemas.car_schema import CarSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions


class BaseQueryOptions(BaseModel):
    page: Optional[int] = Field(default=1, gt=0, description="Page number")
    per_page: Optional[PerPageOptions] = Field(default=10, description="Number of records per page")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: Optional[SortOrderOptions] = Field(
        default="asc", description="Order of sorting. asc for ascending and desc for descending"
    )


class CarQueryOptions(BaseQueryOptions):
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
