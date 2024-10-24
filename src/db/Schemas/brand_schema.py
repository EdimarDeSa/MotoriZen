import uuid

from sqlalchemy import INTEGER, String
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class BrandSchema(BaseSchema):
    __tablename__ = "tb_brand"

    id_brand: MappedColumn[uuid.UUID] = mapped_column(INTEGER(), primary_key=True, autoincrement="auto")
    name: MappedColumn[str] = mapped_column(String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"BrandSchema({self.as_dict()!r})"

    def __str__(self) -> str:
        return f"{self.id_brand} - {self.name}"
