from typing import Any

from sqlalchemy import ColumnElement, func

from DB.Schemas.register_schema import RegisterSchema


class ReportQuerys:
    @property
    def fuel_comsumpted(self) -> ColumnElement[float]:
        return RegisterSchema.distance / RegisterSchema.mean_consuption

    @property
    def consumption_per_trip(self) -> Any:
        return self.fuel_comsumpted / RegisterSchema.number_of_trips

    @property
    def working_time_per_hour(self) -> Any:
        return self.working_time_epoch / 3600

    @property
    def working_time_per_minute(self) -> Any:
        return self.working_time_epoch / 60

    @property
    def total_consumption(self) -> Any:
        return func.sum(self.fuel_comsumpted)

    @property
    def total_distance(self) -> Any:
        return func.sum(RegisterSchema.distance)

    @property
    def total_working_time(self) -> Any:
        return func.sum(RegisterSchema.working_time)

    @property
    def total_number_of_trips(self) -> Any:
        return func.sum(RegisterSchema.number_of_trips)

    @property
    def total_value_received(self) -> Any:
        return func.sum(RegisterSchema.total_value)

    @property
    def mean_consuption_per_distance(self) -> Any:
        return func.avg(self.fuel_comsumpted)

    @property
    def mean_consuption_per_trip(self) -> Any:
        return func.avg(self.consumption_per_trip)

    @property
    def working_time_epoch(self) -> Any:
        return func.extract("epoch", RegisterSchema.working_time)

    @property
    def working_time_hourly(self) -> Any:
        return func.extract("epoch", RegisterSchema.working_time) / 3600

    @property
    def working_time_minutely(self) -> Any:
        return func.extract("epoch", RegisterSchema.working_time) / 60

    @property
    def mean_consuption_per_working_hour(self) -> Any:
        return func.avg(self.fuel_comsumpted / self.working_time_hourly)

    @property
    def mean_consuption_per_working_minute(self) -> Any:
        return func.avg(self.fuel_comsumpted / self.working_time_minutely)

    @property
    def mean_distance(self) -> Any:
        return func.avg(RegisterSchema.distance)

    @property
    def mean_number_of_trips(self) -> Any:
        return func.avg(RegisterSchema.number_of_trips)

    @property
    def mean_value_received(self) -> Any:
        return func.avg(RegisterSchema.total_value)

    @property
    def mean_working_time(self) -> Any:
        return func.avg(RegisterSchema.working_time)

    @property
    def mean_working_time_per_trip(self) -> Any:
        return func.avg(RegisterSchema.working_time / RegisterSchema.number_of_trips)

    @property
    def mean_value_received_per_distance(self) -> Any:
        return func.avg(RegisterSchema.total_value / RegisterSchema.distance)

    @property
    def mean_value_received_per_trip(self) -> Any:
        return func.avg(RegisterSchema.total_value / RegisterSchema.number_of_trips)

    @property
    def mean_value_received_per_consumption(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.fuel_comsumpted)

    @property
    def mean_value_received_per_working_hour(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.working_time_hourly)

    @property
    def mean_value_received_per_working_minute(self) -> Any:
        return func.avg(RegisterSchema.total_value / self.working_time_minutely)
