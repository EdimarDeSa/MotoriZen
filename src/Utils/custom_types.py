from typing import Annotated, Any, Sequence, TypedDict

from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware

from DB.Models import UserModel
from Routers.base_router import BaseRouter
from Services.auth_service import AuthService

PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentActiveUser = Annotated[UserModel, Depends(AuthService().get_current_active_user)]


class MiddlewareRegister(TypedDict):
    middleware_class: type[BaseHTTPMiddleware | CORSMiddleware]
    options: dict[str, Any]


MiddlewareSequence = Sequence[MiddlewareRegister]

RoutersSequence = Sequence[type[BaseRouter]]
