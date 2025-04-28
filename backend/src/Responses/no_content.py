from typing import Mapping

from fastapi import BackgroundTasks

from Responses.base_response import BaseResponse


class NoContent(BaseResponse):
    def __init__(
        self,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = "application/json",
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            content=None,
            status_code=204,
            headers=headers,
            media_type=media_type,
            background=background,
        )
