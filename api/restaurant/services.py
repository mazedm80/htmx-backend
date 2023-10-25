from typing import List, Optional

from api.restaurant.schemas import Restaurant, Table
from core.database.services.restaurants import (
    delete_restaurant,
    delete_table,
    get_restaurant,
    get_tables,
    insert_restaurant,
    insert_table,
    update_restaurant,
    update_table,
)


async def fetch_restaurant(user_id: Optional[int]) -> List[Restaurant]:
    restaurants = await get_restaurant(user_id=user_id)
    return restaurants


async def create_restaurant(restaurant: Restaurant, user_id: int) -> None:
    restaurant = await insert_restaurant(restaurant=restaurant, user_id=user_id)


async def modify_restaurant(
    restaurant: Restaurant, restaurant_id: int, user_id: int
) -> Restaurant:
    restaurant = await update_restaurant(
        restaurant=restaurant, restaurant_id=restaurant_id, user_id=user_id
    )
    return restaurant


async def remove_restaurant(restaurant_id: int, user_id: int) -> None:
    await delete_restaurant(restaurant_id=restaurant_id, user_id=user_id)


async def fetch_tables(restaurant_id: int, user_id: int) -> List[Table]:
    tables = await get_tables(restaurant_id=restaurant_id, user_id=user_id)
    return tables


async def create_table(table: Table, restaurant_id: int, user_id: int) -> None:
    await insert_table(table=table, restaurant_id=restaurant_id, user_id=user_id)


async def modify_table(table: Table, restaurant_id: int, user_id: int) -> Table:
    table = await update_table(
        table=table, restaurant_id=restaurant_id, user_id=user_id
    )
    return table


async def remove_table(table_id: int, restaurant_id: int, user_id: int) -> None:
    await delete_table(table_id=table_id, restaurant_id=restaurant_id, user_id=user_id)
