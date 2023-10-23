from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.auth.models import Permission, Token, TokenData
from core.base.error import UnauthorizedException, ValidationException
from core.database.services.users import get_user_permission

SECRET_KEY = "19436de93dbb87f401018768c42104e6f1a8e7b585f660e74630b8424a6cfbe2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> Annotated[str, "Create access token"]:
    to_encode = data.copy()
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        return None
    return encoded_jwt


async def get_current_user(token: Token = Depends(oauth2_scheme)) -> str:
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

    async def __call__(self, email: str = Depends(get_current_user)) -> TokenData:
        token_data = await get_user_permission(email=email)
        if token_data is None:
            raise ValidationException
        if token_data.auth_group not in self.permission.groups:
            raise UnauthorizedException
        return token_data
