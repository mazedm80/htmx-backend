from core.auth.models import Token
from core.auth.services import create_access_token
from core.base.error import UnauthorizedException
from core.database.services.users import verify_user


async def get_access_token(username: str, password: str) -> Token:
    """Get access token"""

    if not await verify_user(username, password):
        raise UnauthorizedException

    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="bearer")
