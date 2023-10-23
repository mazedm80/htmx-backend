from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class AuthGroup(int, Enum):
    """Auth group enum."""

    SUPER_ADMIN = 1
    ADMIN = 2
    OWNER = 3
    MANAGER = 4
    STAFF = 5
    CUSTOMER = 6


class Permission(BaseModel):
    """Permission schema."""

    groups: List[AuthGroup] = Field(description="Permissions of the user groups.")


class Token(BaseModel):
    """Token schema."""

    access_token: str = Field(description="Access token.")
    token_type: str = Field(description="Token type.")


class TokenData(BaseModel):
    """Token data schema."""

    email: str = Field(description="Email address of the user.")
    user_id: int = Field(description="User id of the user.")
    auth_group: AuthGroup = Field(description="Auth group of the user.")
