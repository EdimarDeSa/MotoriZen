from typing import Any

from sqlalchemy import func

from DB.Querys.base_query_manager import BaseQueryManager

from ..Schemas import RegisterSchema


class RegisterQueryManager(BaseQueryManager):
    ### Distance Reports ###
    def mean_distance(self) -> Any:
        return func.avg(RegisterSchema.distance)

    def mean_distance_per_trip(self) -> Any:
        return func.avg(RegisterSchema.distance / RegisterSchema.number_of_trips)

    def mean_distance_per_working_hour(self) -> Any:
        return func.avg(RegisterSchema.distance / self.working_time_per_hour)

    def mean_distance_per_working_minute(self) -> Any:
        return func.avg(RegisterSchema.distance / self.working_time_per_minute)

    def total_distance(self) -> Any:
        return func.sum(RegisterSchema.distance)

    ### Working Time Reports ###
    def mean_working_time(self) -> Any:
        return func.avg(RegisterSchema.working_time)

    def mean_working_time_per_trip(self) -> Any:
        return func.avg(RegisterSchema.working_time / RegisterSchema.number_of_trips)

    def mean_working_time_per_distance(self) -> Any:
        return func.avg(RegisterSchema.working_time / RegisterSchema.distance)

    def total_working_time(self) -> Any:
        return func.sum(RegisterSchema.working_time)

    ### Consumption Reports ###
    def mean_consumption_per_distance(self) -> Any:
        return func.avg(self.fuel_consumpted)

    def mean_consumption_per_trip(self) -> Any:
        return func.avg(self.fuel_consumpted / RegisterSchema.number_of_trips)

    def mean_consumption_per_working_hour(self) -> Any:
        return func.avg(self.fuel_consumpted / self.working_time_per_hour)

    def mean_consumption_per_working_minute(self) -> Any:
        return func.avg(self.fuel_consumpted / self.working_time_per_minute)

    def total_consumption(self) -> Any:
        return func.sum(self.fuel_consumpted)

    def total_consumption_per_trip(self) -> Any:
        return func.sum(self.fuel_consumpted / RegisterSchema.number_of_trips)

    ### Value Reports ###
    def mean_value_received(self) -> Any:
        return func.avg(RegisterSchema.total_value)

    def mean_value_received_per_consumption(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.fuel_consumpted)

    def mean_value_received_per_distance(self) -> Any:
        return func.avg(RegisterSchema.total_value / RegisterSchema.distance)

    def mean_value_received_per_trip(self) -> Any:
        return func.avg(RegisterSchema.total_value / RegisterSchema.number_of_trips)

    def mean_value_received_per_working_hour(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.working_time_per_hour)

    def mean_value_received_per_working_minute(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.working_time_per_minute)

    def total_value_received(self) -> Any:
        return func.sum(RegisterSchema.total_value)

    ### Number of Trips Reports ###
    def mean_number_of_trips(self) -> Any:
        return func.avg(RegisterSchema.number_of_trips)

    def mean_number_of_trips_per_working_hour(self) -> Any:
        return func.avg(RegisterSchema.number_of_trips / self.working_time_per_hour)

    def mean_number_of_trips_per_working_minute(self) -> Any:
        return func.avg(RegisterSchema.number_of_trips / self.working_time_per_minute)

    def mean_number_of_trips_per_10_km(self) -> Any:
        return func.avg(RegisterSchema.number_of_trips / (RegisterSchema.distance / 10))

    def total_number_of_trips(self) -> Any:
        return func.sum(RegisterSchema.number_of_trips)
