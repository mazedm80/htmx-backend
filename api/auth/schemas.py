from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """User login schema"""

    email: str = Field(
        description="Email address of the user. It must be unique.",
        min_length=5,
        max_length=50,
    )
    password: str = Field(
        description="Password of the user. It must be between 8 and 50 characters.",
        min_length=8,
        max_length=50,
    )


class UserRegister(UserLogin):
    """User register schema"""

    name: str = Field(
        description="Name of the user. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    password2: str = Field(
        description="Password confirmation of the user. It must be between 8 and 50 characters.",
        min_length=8,
        max_length=50,
    )


class UserUpdate(UserRegister):
    """User update schema"""

    name: str = Field(
        description="Name of the user. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    password: str = Field(
        description="Password of the user. It must be between 8 and 50 characters.",
        min_length=8,
        max_length=50,
    )
    password2: str = Field(
        description="Password confirmation of the user. It must be between 8 and 50 characters.",
        min_length=8,
        max_length=50,
    )


class Token(BaseModel):
    """Token schema"""

    access_token: str = Field(description="Access token")
    token_type: str = Field(description="Token type")


class TokenData(BaseModel):
    """Token data schema"""

    email: str = Field(description="Email address of the user")
    name: str = Field(description="Name of the user")
    is_active: bool = Field(description="Is the user active?")
    is_superuser: bool = Field(description="Is the user a superuser?")
    scopes: str = Field(description="Scopes of the user")
