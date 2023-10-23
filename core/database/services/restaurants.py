from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from api.restaurant.schemas import Restaurant
from core.base.error import (
    DatabaseInsertException,
    DatabaseQueryException,
    UnauthorizedException,
)
from core.database import PSQLHandler
from core.database.orm.restaurants import RestaurantAccessTB, RestaurantTB


async def get_access_permissions(user_id: int, restaurant_id: int) -> bool:
    statement = (
        select(RestaurantAccessTB.id)
        .where(RestaurantAccessTB.user_id == user_id)
        .where(RestaurantAccessTB.restaurant_id == restaurant_id)
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    restaurant_access = query.scalar()
    if restaurant_access is None:
        return False
    return True


async def get_all_restaurants(user_id: Optional[int] = None) -> List[Restaurant]:
    if user_id is None:
        statement = select(RestaurantTB)
    else:
        statement = (
            select(RestaurantTB)
            .join(
                RestaurantAccessTB,
                RestaurantAccessTB.restaurant_id == RestaurantTB.id,
            )
            .where(RestaurantAccessTB.user_id == user_id)
        )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    restaurants = query.scalars()
    restaurants_list = []
    for restaurant in restaurants:
        restaurants_list.append(
            Restaurant(
                id=restaurant.id,
                name=restaurant.name,
                address=restaurant.address,
                phone=restaurant.phone,
                email=restaurant.email,
                website=restaurant.website,
                image=restaurant.image,
            )
        )
    return restaurants_list


async def insert_restaurant(restaurant: Restaurant, user_id: int) -> None:
    statement = insert(RestaurantTB).values(
        name=restaurant.name,
        address=restaurant.address,
        phone=restaurant.phone,
        email=restaurant.email,
        website=restaurant.website,
        image=restaurant.image,
    )
    try:
        response = await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    if response is None:
        raise DatabaseInsertException
    statement = insert(RestaurantAccessTB).values(
        user_id=user_id, restaurant_id=response.inserted_primary_key[0]
    )
    try:
        response = await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException


async def update_restaurant_by_id(
    restaurant: Restaurant, restaurant_id: int, user_id: int
) -> Restaurant:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        update(RestaurantTB)
        .where(RestaurantTB.id == restaurant_id)
        .values(
            name=restaurant.name,
            address=restaurant.address,
            phone=restaurant.phone,
            email=restaurant.email,
            website=restaurant.website,
            image=restaurant.image,
        )
    )
    try:
        response = await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    if response is None:
        raise DatabaseInsertException
    statement = select(RestaurantTB).where(RestaurantTB.id == restaurant_id)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    restaurant = query.scalar()
    if restaurant is None:
        raise DatabaseQueryException

    return Restaurant(
        id=restaurant.id,
        name=restaurant.name,
        address=restaurant.address,
        phone=restaurant.phone,
        email=restaurant.email,
        website=restaurant.website,
        image=restaurant.image,
    )


async def delete_restaurant_by_id(restaurant_id: int, user_id: int) -> None:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        delete(RestaurantTB)
        .where(RestaurantTB.id == restaurant_id)
        .returning(RestaurantTB.id)
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
