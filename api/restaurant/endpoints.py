from core.auth.models import AuthGroup, Permission, Token
from core.auth.services import PermissionChecker
from fastapi import APIRouter, Depends, HTTPException, Security, status

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


# permission for admin, manager, waiter
@router.get("/restaurant")
async def get_restaurant(
    authorize: bool = Depends(
        PermissionChecker(Permission(groups=[AuthGroup.SUPER_ADMIN, AuthGroup.ADMIN]))
    ),
):
    if authorize:
        return {"restaurant": "restaurant"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to access",
        headers={"WWW-Authenticate": "Bearer"},
    )
