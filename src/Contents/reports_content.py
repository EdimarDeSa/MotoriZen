import uuid
from typing import Any, Literal

from pydantic import Field

from Contents.base_content import BaseContent


class ReportsContent(BaseContent):
    data: dict[uuid.UUID | Literal["-1"], dict[str, Any]] = Field(
        default_factory=dict, description="Return data, if any"
    )
