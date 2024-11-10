from sqlalchemy import Select, Update, select, update

from DB.Querys.base_query_manager import BaseQueryManager

from ..Schemas import CarSchema


class CarQueryManager(BaseQueryManager):
    def select_last_odometer(self, id_user: str, id_car: str) -> Select[tuple[float]]:
        return select(CarSchema.odometer).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car)

    def update_car_odometer(self, id_user: str, id_car: str, odometer: float) -> Update:
        return (
            update(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car).values(odometer=odometer)
        )
