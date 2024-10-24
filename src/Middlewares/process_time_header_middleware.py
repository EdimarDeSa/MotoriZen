import time
from typing import Any, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Response:
        start_time = time.time()
        response = await call_next(request)  # Esta chamada é assíncrona
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        return response
