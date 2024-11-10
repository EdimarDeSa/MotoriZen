from typing import Any, Mapping

from fastapi import BackgroundTasks

from Responses.base_response import BaseResponse


class Created(BaseResponse):
    def __init__(
        self,
        content: Any | None = None,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = "application/json",
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            content=content,
            status_code=201,
            headers=headers,
            media_type=media_type,
            background=background,
        )
