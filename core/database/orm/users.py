from sqlalchemy import BOOLEAN, INTEGER, TEXT, Column, DateTime, ForeignKey, func

from core.database import Base


class User(Base):
    """User model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(TEXT, unique=True, nullable=False)
    name = Column(TEXT, nullable=False)
    dob = Column(DateTime, nullable=False)
    password = Column(TEXT, nullable=False)
    is_active = Column(BOOLEAN, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


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
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
