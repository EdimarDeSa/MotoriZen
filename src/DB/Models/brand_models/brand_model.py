from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class BrandModel(BaseModel):
    id_brand: int = Field(description=ModelsDescriptionTexts.ID_BRAND)
    name: str = Field(description=ModelsDescriptionTexts.BRAND_NAME)
