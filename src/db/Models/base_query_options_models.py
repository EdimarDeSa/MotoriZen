from typing import Optional

from pydantic import BaseModel, Field

from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions


class BaseQueryOptionsModel(BaseModel):
    page: Optional[int] = Field(default=1, gt=0, description="Page number")
    per_page: Optional[PerPageOptions] = Field(default=10, description="Number of records per page")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: Optional[SortOrderOptions] = Field(
        default="asc", description="Order of sorting. asc for ascending and desc for descending"
    )
