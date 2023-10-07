from core.auth.models import TokenData
from core.database import PSQLHandler
from core.database.orm.user import User, UserPermission
from sqlalchemy import select


async def verify_user(email: str, password: str) -> bool:
    statement = select(User).where(User.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        print("Error while executing query")
    user = query.fetchone()[0]
    if user:
        print(f"username: {user.email}, password: {user.password}")
        return user.password == password
    return False


async def get_user_permission(email: str) -> TokenData:
    statement = select(UserPermission).where(UserPermission.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        print("Error while executing query")
    user = query.fetchone()[0]
    if user:
        return TokenData(email=user.email, auth_group=user.group_id)
    return None
