from typing import List, Optional

from api.menu.schemas import MenuCategory, MenuCategoryList, MenuItem, MenuItemList
from core.database.services.menus import (
    delete_menu_category,
    delete_menu_item,
    get_menu_categories,
    get_menu_category,
    get_menu_items,
    insert_menu_category,
    insert_menu_item,
    update_menu_category,
    update_menu_item,
)


# Menu Category Services
async def fetch_menu_categories(user_id: Optional[int] = None) -> MenuCategoryList:
    return await get_menu_categories(user_id=user_id)


async def fetch_menu_category(category_id: int) -> MenuCategoryList:
    return await get_menu_category(category_id=category_id)


async def create_menu_category(user_id: int, menu_category: MenuCategory) -> None:
    await insert_menu_category(user_id=user_id, menu_category=menu_category)


async def modify_menu_category(user_id: int, menu_category: MenuCategory) -> None:
    await update_menu_category(user_id=user_id, menu_category=menu_category)


async def remove_menu_category(user_id: int, category_id: int) -> None:
    await delete_menu_category(user_id=user_id, category_id=category_id)


# Menu Item Services
async def fetch_menu_items(user_id: int, menu_id: Optional[int] = None) -> MenuItemList:
    return await get_menu_items(user_id=user_id, menu_id=menu_id)


async def create_menu_item(user_id: int, menu_item: MenuItem) -> None:
    await insert_menu_item(user_id=user_id, menu_item=menu_item)


async def modify_menu_item(user_id: int, menu_item: MenuItem) -> None:
    await update_menu_item(user_id=user_id, menu_item=menu_item)


async def remove_menu_item(user_id: int, menu_id: int) -> None:
    await delete_menu_item(user_id=user_id, menu_id=menu_id)
