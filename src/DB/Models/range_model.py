from typing import Generic, Optional

from pydantic import BaseModel, Field

from Utils.custom_primitive_types import T


class RangeModel(BaseModel, Generic[T]):
    start: Optional[T] = Field(default=None, description="Start of the range")
    end: Optional[T] = Field(default=None, description="End of the range")
    # step: Optional[T] = Field(default=None, description="Step of the range")
