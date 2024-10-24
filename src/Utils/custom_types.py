from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from db.Models.user_model import UserModel
from Services.auth_service import AuthService

PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentActiveUser = Annotated[UserModel, Depends(AuthService().get_current_active_user)]
