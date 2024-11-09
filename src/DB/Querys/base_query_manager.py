import uuid
from datetime import date
from typing import Any, Sequence

from pydantic import BaseModel, InstanceOf
from sqlalchemy import Label, Null, Select, func, null, select, true

from DB.Models.range_model import RangeModel
from Enums import AggregationIntervalEnum
from Utils.constants import ASCENDANT, CAR_LABEL, PERIODE_START_DATE
from Utils.custom_primitive_types import Table

from ..Schemas import RegisterSchema


class BaseQueryManager:
    @property
    def fuel_consumpted(self) -> Any:
        return RegisterSchema.distance / RegisterSchema.mean_consuption

    @property
    def consumption_per_trip(self) -> Any:
        return self.fuel_consumpted / RegisterSchema.number_of_trips

    @property
    def working_time_epoch(self) -> Any:
        return func.extract("epoch", RegisterSchema.working_time)

    @property
    def working_time_per_hour(self) -> Any:
        return self.working_time_epoch / 3600

    @property
    def working_time_per_minute(self) -> Any:
        return self.working_time_epoch / 60

    @property
    def null(self) -> Null:
        return null()

    def select_reports(
        cls, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report_query: list[Label[Any]]
    ) -> Select[tuple[uuid.UUID, Any]]:
        return (
            select(RegisterSchema.cd_car.label(CAR_LABEL), *report_query)
            .where(
                RegisterSchema.cd_user == id_user,
                RegisterSchema.cd_car.in_(car_ids) if car_ids else true(),
                RegisterSchema.register_date.between(date_.start, date_.end),
            )
            .group_by(RegisterSchema.cd_car)
        )

    def select_periodicaly_report(
        self,
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        aggregation_interval: AggregationIntervalEnum,
        report_list: list[Label[Any]],
    ) -> Select[tuple[uuid.UUID, Any]]:
        return (
            select(
                RegisterSchema.cd_car.label(CAR_LABEL),
                func.date_trunc(aggregation_interval, RegisterSchema.register_date).label(PERIODE_START_DATE),
                *report_list,
            )
            .where(
                RegisterSchema.cd_user == id_user,
                RegisterSchema.cd_car.in_(car_ids) if car_ids else true(),
                RegisterSchema.register_date.between(date_.start, date_.end),
            )
            .group_by(RegisterSchema.cd_car, func.date_trunc(aggregation_interval, RegisterSchema.register_date))
            .order_by(PERIODE_START_DATE)
        )

    def calculate_offset(cls, per_page: int | None, page: int | None) -> int:
        if per_page is None:
            per_page = 10

        if page is None:
            page = 1

        return per_page * (page - 1)

    def check_order_by(cls, table: Table, sort_by: str | None, sort_order: str | None) -> Any:
        if sort_by is None:
            sort_by = "id_" + table.__tablename__[3:]

        column = getattr(table, sort_by)

        if sort_order is None:
            sort_order = ASCENDANT

        return column.asc() if sort_order == ASCENDANT else column.desc()

    def crete_data_filter(cls, table: Table, id_user: str, query_filters: InstanceOf[BaseModel]) -> list[Any]:
        filters = [table.cd_user == id_user]

        if not query_filters.model_fields_set:
            return filters

        for key in query_filters.model_fields_set:
            if not hasattr(table, key):
                continue

            value = getattr(query_filters, key)

            table_column = getattr(table, key)

            if isinstance(value, RangeModel):

                filters.append(table_column >= value.start)

                if value.end is not None:
                    filters.append(table_column <= value.end)

                continue

            filters.append(table_column == value)

        return filters
