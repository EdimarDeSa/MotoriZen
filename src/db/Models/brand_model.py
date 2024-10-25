from pydantic import BaseModel


class BrandModel(BaseModel):
    id_brand: int
    name: str
