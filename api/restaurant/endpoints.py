from typing import Optional

from fastapi import APIRouter, Depends

from api.restaurant.schemas import Restaurant, RestaurantsList, Table, TablesList
from api.restaurant.services import (
    create_restaurant,
    create_table,
    fetch_restaurant,
    fetch_tables,
    modify_restaurant,
    modify_table,
    remove_restaurant,
    remove_table,
)
from core.auth.models import AuthGroup, Permission, TokenData
from core.auth.services import PermissionChecker
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


@router.get("")
async def get_restaurants(
    restaurant_id: Optional[int] = None,
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
    if authorize.user_id:
        restaurants = await fetch_restaurant(
            user_id=authorize.user_id, restaurant_id=restaurant_id
        )
        return RestaurantsList(restaurants=restaurants)
    raise UnauthorizedException


@router.post("")
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
) -> None:
    if authorize.user_id:
        await create_restaurant(restaurant=restaurant, user_id=authorize.user_id)
        return None
    raise UnauthorizedException


@router.put("")
async def put_restaurant(
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
) -> None:
    if authorize.user_id:
        await modify_restaurant(
            restaurant=restaurant,
            user_id=authorize.user_id,
        )
        return None
    raise UnauthorizedException


@router.delete("")
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
) -> None:
    if authorize.user_id:
        await remove_restaurant(restaurant_id=restaurant_id, user_id=authorize.user_id)
        return None
    raise UnauthorizedException


# Restaurant table
@router.get("/table/{restaurant_id}")
async def get_tables(
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
) -> TablesList:
    if authorize.user_id:
        tables = await fetch_tables(
            restaurant_id=restaurant_id, user_id=authorize.user_id
        )
        return TablesList(tables=tables)
    raise UnauthorizedException


@router.post("/table/{restaurant_id}")
async def add_table(
    restaurant_id: int,
    table: Table,
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
        await create_table(
            restaurant_id=restaurant_id, table=table, user_id=authorize.user_id
        )
        return {"message": "Table added successfully"}
    raise UnauthorizedException


@router.put("/table/{restaurant_id}")
async def put_table(
    restaurant_id: int,
    table: Table,
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
) -> Table:
    if authorize.user_id:
        table = await modify_table(
            restaurant_id=restaurant_id, table=table, user_id=authorize.user_id
        )
        return table
    raise UnauthorizedException


@router.delete("/table/{restaurant_id}")
async def delete_table(
    restaurant_id: int,
    table_id: int,
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
        await remove_table(
            restaurant_id=restaurant_id, table_id=table_id, user_id=authorize.user_id
        )
        return {"message": "Table deleted successfully"}
    raise UnauthorizedException
