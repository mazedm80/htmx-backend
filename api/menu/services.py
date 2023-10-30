from typing import List, Optional

from api.restaurant.schemas import Restaurant
from core.database.services.menus import (
    delete_menu_category,
    delete_menu_item,
    get_menu_categories,
    get_menu_items,
    insert_menu_category,
    insert_menu_item,
    update_menu_category,
    update_menu_item,
)


async def fetch_menu_categories(
    user_id: Optional[int] = None, restaurant_id: Optional[int] = None
) -> List[Restaurant]:
    return await get_menu_categories(user_id=user_id, restaurant_id=restaurant_id)


async def create_menu_category(
    user_id: int, restaurant_id: int, menu_category: Restaurant
) -> None:
    await insert_menu_category(
        user_id=user_id, restaurant_id=restaurant_id, menu_category=menu_category
    )


async def modify_menu_category(
    user_id: int, restaurant_id: int, menu_category: Restaurant
) -> None:
    await update_menu_category(
        user_id=user_id, restaurant_id=restaurant_id, menu_category=menu_category
    )


async def remove_menu_category(
    user_id: int, restaurant_id: int, menu_category: Restaurant
) -> None:
    await delete_menu_category(
        user_id=user_id, restaurant_id=restaurant_id, menu_category=menu_category
    )


async def fetch_menu_items(
    user_id: int, restaurant_id: Optional[int] = None
) -> List[Restaurant]:
    return await get_menu_items(user_id=user_id, restaurant_id=restaurant_id)


async def create_menu_item(
    user_id: int, restaurant_id: int, menu_item: Restaurant
) -> None:
    await insert_menu_item(
        user_id=user_id, restaurant_id=restaurant_id, menu_item=menu_item
    )


async def modify_menu_item(
    user_id: int, restaurant_id: int, menu_item: Restaurant
) -> None:
    await update_menu_item(
        user_id=user_id, restaurant_id=restaurant_id, menu_item=menu_item
    )


async def remove_menu_item(
    user_id: int, restaurant_id: int, menu_item: Restaurant
) -> None:
    await delete_menu_item(
        user_id=user_id, restaurant_id=restaurant_id, menu_item=menu_item
    )
