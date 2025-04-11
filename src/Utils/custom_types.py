from typing import Annotated, Any, Sequence

from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_sessions.middleware import SessionMiddleware
from typing_extensions import TypedDict

from db.Models import UserAuthModel
from Routers.base_router import BaseRouter
from Services.auth_service import AuthService
from Utils.custom_primitive_types import HealthStatusType

PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentActiveUser = Annotated[UserAuthModel, Depends(AuthService().get_current_active_user)]


class MiddlewareRegister(TypedDict):
    middleware_class: type[BaseHTTPMiddleware | CORSMiddleware | SessionMiddleware]
    options: dict[str, Any]


MiddlewareSequence = Sequence[MiddlewareRegister]

RoutersSequence = Sequence[type[BaseRouter]]


class HealthStatus(TypedDict):
    status: HealthStatusType
    message: str | None
