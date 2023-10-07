from core.database import Base
from sqlalchemy import BOOLEAN, INTEGER, TEXT, Column, DateTime, ForeignKey


class User(Base):
    """User model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(TEXT, unique=True, nullable=False)
    name = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    is_active = Column(BOOLEAN, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class AuthGroup(Base):
    """AuthGroup model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "auth_group"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)


class UserPermission(Base):
    """UserPermission model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "user_permissions"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(
        INTEGER, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False
    )
    permission_id = Column(
        INTEGER,
        ForeignKey("public.auth_group.id", ondelete="CASCADE"),
        nullable=False,
        default=6,
    )
