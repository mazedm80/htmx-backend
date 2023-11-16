from typing import Dict

from fastapi import APIRouter, Depends

from api.auth.schemas import User, UserLogin, UserRegister, UserUpdate
from api.auth.services import fetch_user, get_access_token, post_user
from core.auth.models import AuthGroup, Permission, Token, TokenData
from core.auth.services import PermissionChecker, http_scheme
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
async def register(user: UserRegister = Depends()):
    """Register endpoint"""

    await post_user(user=user)
    return {"message": "User created successfully"}


@router.get("/me", response_model=User)
async def me(
    authorize: TokenData = Depends(
        PermissionChecker(
            Permission(
                groups=[
                    AuthGroup.SUPER_ADMIN,
                    AuthGroup.ADMIN,
                    AuthGroup.OWNER,
                    AuthGroup.MANAGER,
                    AuthGroup.STAFF,
                ]
            )
        )
    )
) -> User:
    """Get current user endpoint"""
    if authorize.user_id:
        user = await fetch_user(
            user_id=authorize.user_id, auth_group=authorize.auth_group
        )
        return user
    else:
        raise UnauthorizedException


@router.get("/verify")
async def verify_token(token: Token = Depends(http_scheme)) -> Dict:
    """Verify token endpoint"""
    if token:
        return {"message": "Token is valid"}
    else:
        raise UnauthorizedException
