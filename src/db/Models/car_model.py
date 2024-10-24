import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from db.Models.base_model import BaseModelDb
from db.Schemas.car_schema import CarSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions


class CarModel(BaseModelDb):
    id_car: uuid.UUID = Field(description="Car id")
    cd_user: uuid.UUID = Field(description="User id")
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(description="Renavam of the car")
    model: str = Field(description="Model of the car")
    year: int = Field(description="Year of the car")
    color: str = Field(description="Color of the car")
    license_plate: str = Field(description="License plate of the car")
    odometer: float = Field(description="Odometer of the car")
    is_active: bool = Field(default=True, description="If the car is active")


class NewCarModel(BaseModel):
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: str = Field(max_length=100, description="Model of the car")
    year: int = Field(lt=(datetime.now().year + 1), description="Year of the car")
    color: str = Field(max_length=25, description="Color of the car")
    license_plate: str = Field(max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=0.0, description="Odometer of the car")
    is_active: bool = Field(default=True, description="If the car is active")


class CarUpdates(BaseModel):
    cd_brand: Optional[int] = Field(default=None, description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: Optional[str] = Field(default=None, max_length=100, description="Model of the car")
    year: Optional[int] = Field(default=None, description="Year of the car")
    color: Optional[str] = Field(default=None, max_length=25, description="Color of the car")
    license_plate: Optional[str] = Field(default=None, max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=None, description="Odometer of the car")
    is_active: Optional[bool] = Field(default=None, description="If the car is active")


class UpdateCarModel(BaseModel):
    id_car: uuid.UUID
    updates: CarUpdates


class CarQueryParams(BaseModel):
    id_car: Optional[uuid.UUID] = Field(default=None, description="Car id")
    cd_brand: Optional[int] = Field(default=None, description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: Optional[str] = Field(default=None, max_length=100, description="Model of the car")
    year: Optional[int] = Field(default=None, description="Year of the car")
    color: Optional[str] = Field(default=None, max_length=25, description="Color of the car")
    license_plate: Optional[str] = Field(default=None, max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=None, description="Odometer of the car")
    is_active: Optional[bool] = Field(default=None, description="If the car is active")


class CarQueryOptions(BaseModel):
    page: Optional[int] = Field(default=1, gt=0, description="Page number")
    per_page: Optional[PerPageOptions] = Field(default=10, description="Number of records per page")
    sort_by: Optional[str] = Field(default="id_car", description="Field to sort by")
    sort_order: Optional[SortOrderOptions] = Field(
        default="asc", description="Order of sorting. asc for ascending and desc for descending"
    )

    @field_validator("sort_by", mode="after")
    def validate_sort_by(cls, value: str) -> str:
        valid_sort_fields = CarSchema.fields()
        if value not in valid_sort_fields:
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_SORT_KEY,
                detail=f"Invalid sort_by key {value}. Valid keys: {', '.join(valid_sort_fields)}",
            ).as_http_response()
        return value


class CarsQueryModel(BaseModel):
    query_params: CarQueryParams = Field(default_factory=CarQueryParams)
    query_options: CarQueryOptions = Field(default_factory=CarQueryOptions)


class CarsQueryResponseModel(BaseModel):
    total_results: int
    cars: list[CarModel]
