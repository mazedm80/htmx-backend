from passlib.context import CryptContext

from sqlalchemy import select, insert

from api.auth.schemas import UserRegister, UserUpdate
from core.auth.models import TokenData
from core.base.error import DatabaseQueryException
from core.database.orm.users import User, UserPermission
from core.database.postgres import PSQLHandler


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_user(email: str, password: str) -> bool:
    statement = select(User).where(User.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.fetchone()[0]
    if user:
        return user.password == verify_password(password)
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


async def email_exists(email: str) -> bool:
    statement = select(User).where(User.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.fetchone()[0]
    if user:
        return True
    return False


async def create_user(user: UserRegister) -> User:
    statement = insert(User).values(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password2),
        dob=user.dob,
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    return query.fetchone()[0]


async def get_user(email: str) -> User:
    statement = select(User).where(User.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    return query.fetchone()[0]
