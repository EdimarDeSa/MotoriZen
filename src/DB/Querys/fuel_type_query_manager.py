from sqlalchemy import Select, select

from DB.Querys.base_query_manager import BaseQueryManager

from ..Schemas import FuelTypeSchema


class FuelTypeQueryManager(BaseQueryManager):
    def select_fuel_types(self) -> Select[tuple[FuelTypeSchema]]:
        return select(FuelTypeSchema)

    def select_fuel_type(self, id_fuel_type: int) -> Select[tuple[FuelTypeSchema]]:
        return select(FuelTypeSchema).where(FuelTypeSchema.id_fuel_type == id_fuel_type)
