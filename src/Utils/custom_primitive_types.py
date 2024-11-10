from __future__ import annotations

import uuid
from typing import Any, Literal, TypeVar

PerPageOptions = Literal[10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000]

SortOrderOptions = Literal["asc", "desc"]

Headers = dict[str, Any]

TableDict = dict[str, Any]

Table = type["BaseSchema"]  # type: ignore

T = TypeVar("T")

DataFrameType = dict[uuid.UUID | Literal["-1"], dict[str, Any]]
