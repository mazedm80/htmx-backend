from api.auth.schemas import User, UserRegister
from core.auth.models import AuthGroup, Token
from core.auth.services import create_access_token
from core.base.error import EmailExistsException, UnauthorizedException
from core.database.services.users import (
    create_user,
    email_exists,
    get_user,
    verify_user,
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


async def fetch_user(user_id: int, auth_group: AuthGroup) -> User:
    user = await get_user(user_id=user_id)
    return User(
        id=user.id,
        name=user.name,
        email=user.email,
        auth_group=auth_group,
    )
