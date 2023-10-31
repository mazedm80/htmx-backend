from api.auth.schemas import User, UserRegister
from core.auth.models import Token
from core.auth.services import create_access_token
from core.base.error import EmailExistsException, UnauthorizedException
from core.database.services.users import (
    email_exists,
    verify_user,
    create_user,
    get_user,
)


async def get_access_token(email: str, password: str) -> Token:
    if not await verify_user(email=email, password=password):
        raise UnauthorizedException
    access_token = create_access_token(data={"sub": email}, expires_delta=None)
    return Token(access_token=access_token, token_type="bearer")


async def post_user(user: UserRegister) -> None:
    if not await email_exists(user.email):
        await create_user(user=user)
    else:
        raise EmailExistsException


async def fetch_user(email: str) -> User:
    return await get_user(email=email)
