from datetime import date

from pydantic import BaseModel, Field, field_validator

from core.auth.models import AuthGroup
from core.base.error import ValidationException


class User(BaseModel):
    """User schema"""

    id: int = Field(description="Id of the user.")
    name: str = Field(
        description="Name of the user. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    email: str = Field(
        description="Email address of the user. It must be unique.",
        min_length=5,
        max_length=50,
    )
    auth_group: AuthGroup = Field(description="Auth group of the user.")


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

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValidationException(detail="invalid email")
        return v


class UserRegister(UserLogin):
    """User register schema"""

    password2: str = Field(
        description="Password confirmation of the user. It must be between 8 and 50 characters.",
        min_length=8,
        max_length=50,
    )

    name: str = Field(
        description="Name of the user. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    dob: date = Field(description="Date of birth of the user.")

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        if " " not in v:
            raise ValidationException(detail="name must contain first and last name")
        v_rem = v.replace(" ", "")
        if not v_rem.isalpha():
            raise ValidationException(detail="name must be alphabetic")
        return v

    @field_validator("dob")
    @classmethod
    def dob_must_be_valid(cls, v):
        if v > date.today():
            raise ValidationException(detail="date of birth must be in the past")
        return v

    @field_validator("password2")
    @classmethod
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValidationException(detail="passwords do not match")
        return v


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
