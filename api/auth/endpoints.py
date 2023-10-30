from fastapi import APIRouter, Depends

from api.auth.schemas import User, UserLogin, UserRegister, UserUpdate
from api.auth.services import get_access_token, post_user, fetch_user
from core.auth.models import Token
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=Token)
async def login(form_data: UserLogin = Depends()):
    """Login endpoint"""

    try:
        token = await get_access_token(form_data.email, form_data.password)
    except Exception:
        raise UnauthorizedException
    return token


@router.post("/register")
async def register(user: UserRegister = Depends()) -> User:
    """Register endpoint"""

    try:
        user = await post_user(user)
    except Exception:
        raise UnauthorizedException
    return user


@router.get("/me", response_model=User)
async def me(user: UserUpdate = Depends()) -> User:
    """Update me endpoint"""

    try:
        user = await fetch_user(user)
    except Exception:
        raise UnauthorizedException
    return user
