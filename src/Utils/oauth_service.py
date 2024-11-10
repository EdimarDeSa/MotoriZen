from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

Oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenSelector = Annotated[str, Depends(Oauth2Scheme)]
