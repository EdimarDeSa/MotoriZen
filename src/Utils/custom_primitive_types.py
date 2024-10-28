from datetime import date, time
from typing import Any, Literal, TypeVar

PerPageOptions = Literal[10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000]

SortOrderOptions = Literal["asc", "desc"]

Headers = dict[str, Any]

T = TypeVar("T")
