import uuid
from datetime import date, time, timedelta
from decimal import Decimal
from typing import Any, Mapping, Sequence

from sqlalchemy import RowMapping


class BaseReportRepository:
    def return_number(self, results: Sequence[RowMapping]) -> Sequence[Mapping[str, uuid.UUID | float | int | str]]:
        return [
            {
                key: (self._round_value(value) if not isinstance(value, uuid.UUID) else value)
                for key, value in result.items()
            }
            for result in results
        ]

    def return_float_to_time(self, results: Sequence[RowMapping]) -> Sequence[Mapping[str, uuid.UUID | str]]:
        return [
            {
                key: value if isinstance(value, uuid.UUID) else self.__float_to_hhmmss(value)
                for key, value in result.items()
            }
            for result in results
        ]

    def return_time(self, results: Sequence[RowMapping]) -> Sequence[Mapping[str, uuid.UUID | str]]:
        return [
            {key: value if isinstance(value, uuid.UUID) else str(value) for key, value in result.items()}
            for result in results
        ]

    def return_periodic(
        self, results: Sequence[RowMapping], report: str, period: timedelta
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:
        return [
            {
                "id_car": result["id_car"],
                report: {
                    "total": self._round_value(result[report]),
                    "initial_date": self.strfdate(result["register_date"]),
                    "final_date": self.strfdate(result["register_date"] + period),
                },
            }
            for result in results
        ]

    def return_not_implemented(self, report: str) -> Sequence[Mapping[str, str]]:
        return [{"id_car": "-1", report: "Not implemented yet"}]

    def default_number(
        self, report: str, car_ids: Sequence[uuid.UUID]
    ) -> Sequence[Mapping[str, uuid.UUID | float | int]]:
        return [{"cd_car": id_car, report: 0} for id_car in car_ids]

    def default_time(self, report: str, car_ids: Sequence[uuid.UUID]) -> Sequence[Mapping[str, uuid.UUID | time]]:
        return [{"cd_car": id_car, report: time(0, 0, 0)} for id_car in car_ids]

    def default_date(
        self, report: str, car_ids: Sequence[uuid.UUID]
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float]]]:
        return [{"cd_car": id_car, report: {self.strfdate(date(2000, 1, 1)): 0.0}} for id_car in car_ids]

    def strfdate(self, date_: date) -> str:
        return date_.strftime(r"%d-%m-%Y")

    def _round_value(self, value: Any) -> int | float | str:
        if not isinstance(value, int | float | Decimal):
            return str(value)

        return value if isinstance(value, int) else round(float(value), 2)

    def __float_to_hhmmss(self, hours: Decimal) -> str:
        hours_float = float(hours)

        td = timedelta(hours=hours_float)

        total_seconds = int(td.total_seconds())
        hh, remainder = divmod(total_seconds, 3600)
        mm, ss = divmod(remainder, 60)
        return f"{hh:02}:{mm:02}:{ss:02}"
