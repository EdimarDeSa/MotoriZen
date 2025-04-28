from sqlalchemy import Select, Update, select, update

from db.Querys.base_query_manager import BaseQueryManager

from ..Schemas import VehicleSchema


class VehicleQueryManager(BaseQueryManager):
    def select_last_odometer(self, id_user: str, id_vehicle: str) -> Select[tuple[float]]:
        return select(VehicleSchema.odometer).where(
            VehicleSchema.cd_user == id_user, VehicleSchema.id_vehicle == id_vehicle
        )

    def update_vehicle_odometer(self, id_user: str, id_vehicle: str, odometer: float) -> Update:
        return (
            update(VehicleSchema)
            .where(VehicleSchema.cd_user == id_user, VehicleSchema.id_vehicle == id_vehicle)
            .values(odometer=odometer)
        )
