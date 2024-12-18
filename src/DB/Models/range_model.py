from typing import Generic, Optional

from pydantic import BaseModel, Field

from Utils.custom_primitive_types import T
from Utils.Internacionalization import ModelsDescriptionTexts


class RangeModel(BaseModel, Generic[T]):
    start: Optional[T] = Field(default=None, description=ModelsDescriptionTexts.RANGE_START)
    end: Optional[T] = Field(default=None, description=ModelsDescriptionTexts.RANGE_END)
