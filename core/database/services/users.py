from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert, dialect

from api.auth.schemas import UserRegister, UserUpdate
from core.auth.models import TokenData
from core.base.error import DatabaseQueryException, DatabaseInsertException
from core.database.orm.users import UserTB, UserPermission
from core.database.postgres import PSQLHandler


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_user(email: str, password: str) -> bool:
    statement = select(UserTB).where(UserTB.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.scalar()
    if user:
        return verify_password(plain_password=password, hashed_password=user.password)
    return False


async def get_user_permission(email: str) -> TokenData:
    user_id = (select(UserTB.id).where(UserTB.email == email)).cte("user_id")

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
    statement = select(UserTB.id).where(UserTB.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    user = query.fetchone()
    if user:
        return True
    return False


async def create_user(user: UserRegister) -> None:
    statement = insert(UserTB).values(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password2),
        dob=user.dob,
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def get_user(email: str) -> UserTB:
    statement = select(UserTB).where(UserTB.email == email)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    return query.fetchone()[0]
