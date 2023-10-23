from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.auth.services import get_access_token
from core.auth.models import Token
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint"""

    try:
        token = await get_access_token(form_data.username, form_data.password)
    except Exception:
        raise UnauthorizedException
    return token
