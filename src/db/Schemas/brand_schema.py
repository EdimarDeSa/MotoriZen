from datetime import datetime

from sqlalchemy import INTEGER, DateTime, String
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class BrandSchema(BaseSchema):
    __tablename__ = "tb_brand"

    id_brand: MappedColumn[int] = mapped_column(INTEGER(), primary_key=True, autoincrement="auto")
    name: MappedColumn[str] = mapped_column(String(20), nullable=False, unique=True)
    updated_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __str__(self) -> str:
        return f"{self.id_column} - {self.name}"
