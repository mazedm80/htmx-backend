from sqlalchemy import select

from core.auth.models import TokenData
from core.base.error import DatabaseQueryException
from core.database.orm.users import User, UserPermission
from core.database.postgres import PSQLHandler


async def verify_user(email: str, password: str) -> bool:
    statement = select(User).where(User.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.fetchone()[0]
    if user:
        return user.password == password
    return False


async def get_user_permission(email: str) -> TokenData:
    user_id = (select(User.id).where(User.email == email)).cte("user_id")

    statement = select(UserPermission.permission_id, UserPermission.user_id).join(
        user_id, user_id.c.id == UserPermission.user_id
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.fetchone()
    if user:
        return TokenData(user_id=user.user_id, auth_group=user.permission_id)
    return None
