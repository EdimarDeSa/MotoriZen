from typing import Any, Mapping

from fastapi import BackgroundTasks
from fastapi.responses import Response

from Contents.base_content import BaseContent


class BaseResponse(Response):
    def __init__(
        self,
        content: BaseContent | None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = "application/json",
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            content=content.model_dump_json(exclude_none=True) if content else None,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
