from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, Request
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from core.auth.models import Permission, Token, TokenData
from core.base.error import UnauthorizedException, ValidationException
from core.database.services.users import get_user_permission

SECRET_KEY = "19436de93dbb87f401018768c42104e6f1a8e7b585f660e74630b8424a6cfbe2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class JWTSCHEME(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Annotated[str, "JWTSCHEME.__call__"]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request=request
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise UnauthorizedException
            if not self.verify(token=credentials.credentials):
                raise UnauthorizedException
            return credentials.credentials
        raise UnauthorizedException

    def verify(self, token: str) -> bool:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return False
        return True


http_scheme = JWTSCHEME()


def create_access_token(
    data: dict, expires_delta: Optional[timedelta]
) -> Annotated[str, "Create access token"]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    issued_at = datetime.utcnow()
    to_encode.update({"iat": issued_at})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        return None
    return encoded_jwt


async def get_user_email_from_token(token: Token = Depends(http_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException
    except JWTError:
        raise ValidationException
    return email


class PermissionChecker:
    def __init__(self, permission: Permission) -> None:
        self.permission = permission

    async def __call__(
        self, email: str = Depends(get_user_email_from_token)
    ) -> TokenData:
        token_data = await get_user_permission(email=email)
        if token_data is None:
            raise ValidationException
        if token_data.auth_group not in self.permission.groups:
            raise UnauthorizedException
        return token_data
