from typing import List, Tuple
from fastapi import APIRouter, Depends, HTTPException, Security, status

from api.restaurant.schemas import Restaurant, RestaurantsList
from api.restaurant.services import create_restaurant, get_restaurant
from core.auth.models import AuthGroup, Permission, Token
from core.auth.services import PermissionChecker

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


# permission for admin, manager, waiter
@router.get("/all")
async def get_all_restaurant(
    authorize: Tuple[bool, str] = Depends(
        PermissionChecker(Permission(groups=[AuthGroup.SUPER_ADMIN, AuthGroup.ADMIN]))
    ),
) -> RestaurantsList:
    permission, _ = authorize
    if permission:
        restaurants = await get_restaurant()
        return RestaurantsList(restaurants=restaurants)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to access",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_a_restaurant(
    restaurant: Restaurant,
    authorize: Tuple[bool, str] = Depends(
        PermissionChecker(
            Permission(
                groups=[
                    AuthGroup.SUPER_ADMIN,
                    AuthGroup.ADMIN,
                    AuthGroup.OWNER,
                    AuthGroup.MANAGER,
                ]
            )
        )
    ),
):
    permission, email = authorize
    if permission:
        try:
            await create_restaurant(restaurant=restaurant, email=email)
            return {"message": "Restaurant created successfully"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error while creating restaurant",
                headers={"WWW-Authenticate": "Bearer"},
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have permission to access",
        headers={"WWW-Authenticate": "Bearer"},
    )
