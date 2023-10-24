from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from api.menu.schemas import MenuCategory, MenuItem
from core.base.error import (
    DatabaseInsertException,
    DatabaseQueryException,
    UnauthorizedException,
)
from core.database.postgres import PSQLHandler
from core.database.orm.menus import (
    MenuCategoryTB,
    MenuItemTB,
)
from core.database.services.restaurants import get_access_permissions


async def get_all_menu_categories(
    user_id: int, restaurant_id: int
) -> List[MenuCategory]:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = select(MenuCategoryTB).where(
        MenuCategoryTB.restaurant_id == restaurant_id
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    menu_categories = query.scalars()
    menu_categories_list = []
    for menu_category in menu_categories:
        menu_categories_list.append(
            MenuCategory(
                id=menu_category.id,
                restaurant_id=menu_category.restaurant_id,
                name=menu_category.name,
            )
        )
    return menu_categories_list


async def insert_menu_category(
    user_id: int, restaurant_id: int, menu_category: MenuCategory
) -> None:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = insert(MenuCategoryTB).values(
        restaurant_id=restaurant_id,
        name=menu_category.name,
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def update_menu_category(
    user_id: int, restaurant_id: int, menu_category: MenuCategory
) -> MenuCategory:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        update(MenuCategoryTB)
        .where(MenuCategoryTB.id == menu_category.id)
        .values(name=menu_category.name)
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return menu_category


async def delete_menu_category(
    user_id: int, restaurant_id: int, menu_category_id: int
) -> None:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = delete(MenuCategoryTB).where(MenuCategoryTB.id == menu_category_id)
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def get_all_menu_items(
    user_id: int, restaurant_id: int, menu_category_id: Optional[int] = None
) -> List[MenuItem]:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    if menu_category_id is None:
        statement = select(MenuItemTB).where(
            MenuItemTB.restaurant_id == restaurant_id,
        )
    else:
        statement = select(MenuItemTB).where(
            MenuItemTB.restaurant_id == restaurant_id,
            MenuItemTB.menu_category_id == menu_category_id,
        )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    menu_items = query.scalars()
    menu_items_list = []
    for menu_item in menu_items:
        menu_items_list.append(
            MenuItem(
                id=menu_item.id,
                restaurant_id=menu_item.restaurant_id,
                menu_category_id=menu_item.menu_category_id,
                name=menu_item.name,
                description=menu_item.description,
                price=menu_item.price,
                vegetarian=menu_item.vegetarian,
                vegan=menu_item.vegan,
                gluten_free=menu_item.gluten_free,
                spicy=menu_item.spicy,
            )
        )
    return menu_items_list


async def insert_menu_item(
    user_id: int, restaurant_id: int, menu_item: MenuItem
) -> None:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = insert(MenuItemTB).values(
        restaurant_id=restaurant_id,
        menu_category_id=menu_item.menu_category_id,
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        vegetarian=menu_item.vegetarian,
        vegan=menu_item.vegan,
        gluten_free=menu_item.gluten_free,
        spicy=menu_item.spicy,
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def update_menu_item(
    user_id: int, restaurant_id: int, menu_item: MenuItem
) -> MenuItem:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = (
        update(MenuItemTB)
        .where(MenuItemTB.id == menu_item.id)
        .values(
            menu_category_id=menu_item.menu_category_id,
            name=menu_item.name,
            description=menu_item.description,
            price=menu_item.price,
            vegetarian=menu_item.vegetarian,
            vegan=menu_item.vegan,
            gluten_free=menu_item.gluten_free,
            spicy=menu_item.spicy,
        )
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return menu_item


async def delete_menu_item(user_id: int, restaurant_id: int, menu_item_id: int) -> None:
    if not await get_access_permissions(user_id=user_id, restaurant_id=restaurant_id):
        raise UnauthorizedException
    statement = delete(MenuItemTB).where(MenuItemTB.id == menu_item_id)
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
