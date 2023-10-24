from fastapi import APIRouter, Depends, status

from api.restaurant.schemas import Restaurant, RestaurantsList
from api.restaurant.services import (
    create_restaurant,
    fetch_restaurant,
    remove_restaurant,
    update_restaurant,
)
from core.auth.models import AuthGroup, Permission, TokenData
from core.auth.services import PermissionChecker
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


# permission for admin, manager, waiter
@router.get("/all")
async def get_restaurants(
    authorize: TokenData = Depends(
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
) -> RestaurantsList:
    user_id = authorize.user_id
    if (
        authorize.auth_group == AuthGroup.SUPER_ADMIN
        or authorize.auth_group == AuthGroup.ADMIN
    ):
        restaurants = await fetch_restaurant(user_id=None)
        return RestaurantsList(restaurants=restaurants)
    elif (
        authorize.auth_group == AuthGroup.OWNER
        or authorize.auth_group == AuthGroup.MANAGER
    ):
        restaurants = await fetch_restaurant(user_id=user_id)
        return RestaurantsList(restaurants=restaurants)
    raise UnauthorizedException


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def post_restaurant(
    restaurant: Restaurant,
    authorize: TokenData = Depends(
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
    if authorize.user_id:
        await create_restaurant(restaurant=restaurant, user_id=authorize.user_id)
        return {"message": "Restaurant created successfully"}
    raise UnauthorizedException


# update restaurant by id
@router.put("/update/{restaurant_id}")
async def put_restaurant(
    restaurant_id: int,
    restaurant: Restaurant,
    authorize: TokenData = Depends(
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
) -> Restaurant:
    if authorize.user_id:
        restaurant = await update_restaurant(
            restaurant_id=restaurant_id,
            restaurant=restaurant,
            user_id=authorize.user_id,
        )
        return restaurant
    raise UnauthorizedException


# delete restaurant by id
@router.delete("/delete/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    authorize: TokenData = Depends(
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
    if authorize.user_id:
        await remove_restaurant(restaurant_id=restaurant_id, user_id=authorize.user_id)
        return {"message": "Restaurant deleted successfully"}
    raise UnauthorizedException
