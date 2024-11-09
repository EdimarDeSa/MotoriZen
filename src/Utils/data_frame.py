import sys
from typing import Literal
from uuid import UUID

from Utils.custom_primitive_types import DataFrameType


class DataFrame(DataFrameType):

    def insert_reports(self, other: DataFrameType) -> None:
        for id_car, reports in other.items():

            if not self.check_car_existence(id_car):
                self[id_car] = dict()

            for report, data in reports.items():
                self[id_car][report] = data

    def check_car_existence(self, id_car: UUID | Literal["-1"]) -> bool:
        return id_car in self.keys()

    @property
    def total_cars(self) -> int:
        return len(self.keys())

    @property
    def total_results(self) -> int:
        total_results = 0
        for key in self.keys():
            total_results += len(self[key])

        return total_results

    @property
    def nbytes(self) -> str:
        total_bites = self._deep_sizeof(self)
        return self._format_bytes(total_bites)

    def _format_bytes(self, size: int | float) -> str:
        units = ["bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0

        while size >= 1024:
            size /= 1024
            unit_index += 1

        return f"{size:,.2f} {units[unit_index]}"

    def _deep_sizeof(self, obj: object, seen: set[int] | None = None) -> int:
        """Calcula o tamanho total de um objeto em bytes, incluindo objetos aninhados."""
        if seen is None:
            seen = set()

        size = sys.getsizeof(obj)
        obj_id = id(obj)

        if obj_id in seen:
            return 0  # Evita contagem duplicada de objetos

        seen.add(obj_id)

        if isinstance(obj, dict):
            size += sum(self._deep_sizeof(k, seen) + self._deep_sizeof(v, seen) for k, v in obj.items())
        elif isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(self._deep_sizeof(i, seen) for i in obj)

        return size
