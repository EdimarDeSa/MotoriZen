from pydantic import BaseModel, ConfigDict, Field


class BrandModel(BaseModel):
    __config__: ConfigDict = Field(description="New register model config")

    id_brand: int = Field(description="Id of the brand")
    name: str = Field(description="Name of the brand")
