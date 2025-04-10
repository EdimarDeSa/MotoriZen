from typing import Optional, Self

from pydantic import BaseModel, Field, model_validator

from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.Internacionalization import ModelsDescriptionTexts


class CarUpdatesDataModel(BaseModel):
    cd_brand: Optional[int] = Field(default=None, description=ModelsDescriptionTexts.CD_BRAND)
    renavam: Optional[str] = Field(default=None, max_length=11, description=ModelsDescriptionTexts.RENAVAM)
    model: Optional[str] = Field(default=None, max_length=100, description=ModelsDescriptionTexts.CAR_MODEL)
    year: Optional[int] = Field(default=None, description=ModelsDescriptionTexts.CAR_YEAR)
    color: Optional[str] = Field(default=None, max_length=25, description=ModelsDescriptionTexts.CAR_COLOR)
    license_plate: Optional[str] = Field(default=None, max_length=10, description=ModelsDescriptionTexts.LICENSE_PLATE)
    odometer: Optional[float] = Field(default=None, description=ModelsDescriptionTexts.ODOMETER)
    is_active: Optional[bool] = Field(default=None, description=ModelsDescriptionTexts.IS_ACTIVE)

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
                detail=ModelsDescriptionTexts.INVALID_UPDATES_DATA,
            )
        return self
