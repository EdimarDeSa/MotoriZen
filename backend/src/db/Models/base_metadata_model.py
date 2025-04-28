import sys
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from Utils.Internacionalization import ModelsDescriptionTexts


class BaseMetadataModel(BaseModel):
    total_results: int = Field(description=ModelsDescriptionTexts.TOTAL_RESULTS)
    total_bytes: Optional[str] = Field(default=None, description=ModelsDescriptionTexts.TOTAL_BYTES)

    @field_validator("total_bytes", mode="after")
    def validate_total_bytes(cls, value: Optional[str]) -> str:
        if value is None:
            return cls.nbytes

        return value

    @property
    def nbytes(self) -> str:
        total_bytes = self._deep_sizeof(self)
        return self._format_bytes(total_bytes)

    def _format_bytes(self, size: int | float) -> str:
        units = ["bytes", "KB", "MB", "GB", "TB"]
        total_units = len(units)
        unit_index = 0

        while size >= 1024:
            size /= 1024
            unit_index += 1

            if unit_index >= total_units:
                break

        return f"{size:,.2f} {units[unit_index]}"

    def _deep_sizeof(self, obj: object, seen: set[int] | None = None) -> int:
        """Calcula o tamanho total de um objeto em bytes, incluindo objetos aninhados."""
        if seen is None:
            seen = set()

        size = sys.getsizeof(obj)
        object_id = id(obj)

        if object_id in seen:
            return 0  # Evita contagem duplicada de objetos

        seen.add(object_id)

        if isinstance(obj, dict):
            size += sum(self._deep_sizeof(k, seen) + self._deep_sizeof(v, seen) for k, v in obj.items())
        elif isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(self._deep_sizeof(i, seen) for i in obj)

        return size
