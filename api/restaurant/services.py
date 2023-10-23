from typing import List, Optional

from api.restaurant.schemas import Restaurant
from core.database.services.restaurants import (
    delete_restaurant_by_id,
    get_all_restaurants,
    insert_restaurant,
    update_restaurant_by_id,
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
