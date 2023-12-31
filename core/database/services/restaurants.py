from typing import List, Optional

from sqlalchemy import delete, select, update, func
from sqlalchemy.dialects.postgresql import insert

from api.restaurant.schemas import Restaurant, Table
from core.base.error import (
    DatabaseInsertException,
    DatabaseQueryException,
    UnauthorizedException,
)
from core.database.orm.restaurants import (
    RestaurantAccessTB,
    RestaurantTableTB,
    RestaurantTB,
)
from core.database.postgres import PSQLHandler


async def access_permission(user_id: int, restaurant_id: int) -> bool:
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


# Restaurant
async def get_restaurant(
    user_id: int, restaurant_id: Optional[int]
) -> List[Restaurant]:
    if restaurant_id is None:
        restaurant_id = select(RestaurantAccessTB.restaurant_id).where(
            RestaurantAccessTB.user_id == user_id
        )
        statement = select(
            RestaurantTB.id,
            RestaurantTB.name,
            RestaurantTB.address,
            RestaurantTB.phone,
            RestaurantTB.email,
            RestaurantTB.website,
            RestaurantTB.image,
        ).filter(RestaurantTB.id.in_(restaurant_id))
    else:
        if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
            raise UnauthorizedException
        statement = select(
            RestaurantTB.id,
            RestaurantTB.name,
            RestaurantTB.address,
            RestaurantTB.phone,
            RestaurantTB.email,
            RestaurantTB.website,
            RestaurantTB.image,
        ).filter(RestaurantTB.id == restaurant_id)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    restaurants = query.fetchall()
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
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def update_restaurant(restaurant: Restaurant, user_id: int) -> None:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant.id):
        raise UnauthorizedException
    statement = (
        update(RestaurantTB)
        .where(RestaurantTB.id == restaurant.id)
        .values(
            name=restaurant.name,
            address=restaurant.address,
            phone=restaurant.phone,
            email=restaurant.email,
            website=restaurant.website,
            image=restaurant.image,
            updated_at=func.now(),
        )
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def delete_restaurant(restaurant_id: int, user_id: int) -> None:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        delete(RestaurantTB)
        .where(RestaurantTB.id == restaurant_id)
        .returning(RestaurantTB.id)
    )
    try:
        response = await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    if response is None:
        raise DatabaseInsertException
    return None


# Table
async def get_tables(restaurant_id: int, user_id: int) -> List[Table]:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = select(RestaurantTableTB).where(
        RestaurantTableTB.restaurant_id == restaurant_id
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    tables = query.scalars()
    tables_list = []
    for table in tables:
        tables_list.append(
            Table(
                table_number=table.table_number,
            )
        )
    return tables_list


async def insert_table(table: Table, restaurant_id: int, user_id: int) -> None:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = insert(RestaurantTableTB).values(
        restaurant_id=restaurant_id,
        table_number=table.table_number,
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def update_table(table: Table, restaurant_id: int, user_id: int) -> Table:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        update(RestaurantTableTB)
        .where(RestaurantTableTB.restaurant_id == restaurant_id)
        .where(RestaurantTableTB.table_number == table.table_number)
        .values(table_number=table.table_number)
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return table


async def delete_table(table_number: int, restaurant_id: int, user_id: int) -> None:
    if not await access_permission(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        delete(RestaurantTableTB)
        .where(RestaurantTableTB.restaurant_id == restaurant_id)
        .where(RestaurantTableTB.table_number == table_number)
        .returning(RestaurantTableTB.id)
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None
