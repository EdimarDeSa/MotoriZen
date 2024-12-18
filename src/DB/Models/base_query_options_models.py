from typing import Optional

from pydantic import BaseModel, Field

from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions
from Utils.Internacionalization import ModelsDescriptionTexts


class BaseQueryOptionsModel(BaseModel):
    page: Optional[int] = Field(default=1, gt=0, description=ModelsDescriptionTexts.PAGE)
    per_page: Optional[PerPageOptions] = Field(default=10, description=ModelsDescriptionTexts.PER_PAGE)
    sort_by: Optional[str] = Field(default=None, description=ModelsDescriptionTexts.SORT_BY)
    sort_order: Optional[SortOrderOptions] = Field(default="asc", description=ModelsDescriptionTexts.SORT_ORDER)
