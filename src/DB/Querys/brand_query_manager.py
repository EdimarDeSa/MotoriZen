from sqlalchemy import Select, select

from DB.Querys.base_query_manager import BaseQueryManager

from ..Schemas import BrandSchema


class BrandQueryManager(BaseQueryManager):
    def select_brands(self) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema)

    def select_brand(self, id_brand: int) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema).where(BrandSchema.id_brand == id_brand)
