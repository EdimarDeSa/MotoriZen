from typing import Optional, Self

from pydantic import BaseModel, Field, model_validator

from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError


class CarUpdatesDataModel(BaseModel):
    cd_brand: Optional[int] = Field(default=None, description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: Optional[str] = Field(default=None, max_length=100, description="Model of the car")
    year: Optional[int] = Field(default=None, description="Year of the car")
    color: Optional[str] = Field(default=None, max_length=25, description="Color of the car")
    license_plate: Optional[str] = Field(default=None, max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=None, description="Odometer of the car")
    is_active: Optional[bool] = Field(default=None, description="If the car is active")

    @model_validator(mode="after")
    def validate_updates_value(self) -> Self:
        if all(
            [
                self.cd_brand is None,
                self.renavam is None,
                self.model is None,
                self.year is None,
                self.color is None,
                self.license_plate is None,
                self.odometer is None,
                self.is_active is None,
            ]
        ):
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_UPDATES_DATA,
                detail="Invalid updates data. Please, provide at least one value to update.",
            )
        return self
