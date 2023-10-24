from fastapi import APIRouter, Depends

from api.restaurant.schemas import Restaurant, RestaurantsList, Table, TablesList
from api.restaurant.services import (
    create_restaurant,
    create_table,
    fetch_restaurant,
    fetch_tables,
    remove_restaurant,
    remove_table,
    update_restaurant,
    update_table,
)
from core.auth.models import AuthGroup, Permission, TokenData
from core.auth.services import PermissionChecker
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


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


@router.post("/create")
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


# Restaurant table
@router.get("/tables/{restaurant_id}")
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


@router.post("/add-table/{restaurant_id}")
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


@router.put("/update-table/{restaurant_id}")
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
        table = await update_table(
            restaurant_id=restaurant_id, table=table, user_id=authorize.user_id
        )
        return table
    raise UnauthorizedException


@router.delete("/delete-table/{restaurant_id}")
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
