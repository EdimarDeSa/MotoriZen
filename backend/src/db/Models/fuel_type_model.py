from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class FuelTypeModel(BaseModel):
    id_fuel_type: int = Field(description=ModelsDescriptionTexts.ID_FUEL_TYPE)
    name: str = Field(description=ModelsDescriptionTexts.FUEL_TYPE_NAME)
