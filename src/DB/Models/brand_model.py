from pydantic import BaseModel, ConfigDict, Field


class BrandModel(BaseModel):

    id_brand: int = Field(description="Id of the brand")
    name: str = Field(description="Name of the brand")
