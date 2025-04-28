from typing import Mapping

from fastapi import BackgroundTasks

from Contents.base_content import BaseContent
from Responses.base_response import BaseResponse


class Ok(BaseResponse):
    def __init__(
        self,
        content: BaseContent,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = "application/json",
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            content=content,
            status_code=200,
            headers=headers,
            media_type=media_type,
            background=background,
        )
