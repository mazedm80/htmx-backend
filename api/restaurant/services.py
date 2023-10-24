from typing import List, Optional

from api.restaurant.schemas import Restaurant, Table
from core.database.services.restaurants import (
    delete_restaurant_by_id,
    delete_table_by_id,
    get_all_restaurants,
    get_tables_by_id,
    insert_restaurant,
    insert_table_by_id,
    update_restaurant_by_id,
    update_table_by_id,
)


async def fetch_restaurant(user_id: Optional[int]) -> List[Restaurant]:
    restaurants = await get_all_restaurants(user_id=user_id)
    return restaurants


async def create_restaurant(restaurant: Restaurant, user_id: int) -> None:
    restaurant = await insert_restaurant(restaurant=restaurant, user_id=user_id)


async def update_restaurant(
    restaurant: Restaurant, restaurant_id: int, user_id: int
) -> Restaurant:
    restaurant = await update_restaurant_by_id(
        restaurant=restaurant, restaurant_id=restaurant_id, user_id=user_id
    )
    return restaurant


async def remove_restaurant(restaurant_id: int, user_id: int) -> None:
    await delete_restaurant_by_id(restaurant_id=restaurant_id, user_id=user_id)


async def fetch_tables(restaurant_id: int, user_id: int) -> List[Table]:
    tables = await get_tables_by_id(restaurant_id=restaurant_id, user_id=user_id)
    return tables


async def fetch_table(restaurant_id: int, user_id: int) -> List[Table]:
    tables = await get_tables_by_id(restaurant_id=restaurant_id, user_id=user_id)
    return tables


async def create_table(table: Table, restaurant_id: int, user_id: int) -> None:
    await insert_table_by_id(table=table, restaurant_id=restaurant_id, user_id=user_id)


async def update_table(table: Table, restaurant_id: int, user_id: int) -> Table:
    table = await update_table_by_id(
        table=table, restaurant_id=restaurant_id, user_id=user_id
    )
    return table


async def remove_table(table_id: int, restaurant_id: int, user_id: int) -> None:
    await delete_table_by_id(
        table_id=table_id, restaurant_id=restaurant_id, user_id=user_id
    )
