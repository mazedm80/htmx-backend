from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from api.menu.schemas import MenuCategory, MenuItem
from core.base.error import DatabaseInsertException, DatabaseQueryException
from core.database.orm.menus import MenuCategoryTB, MenuItemTB
from core.database.postgres import PSQLHandler


async def get_menu_categories(user_id: int) -> List[MenuCategory]:
    if user_id is None:
        statement = select(MenuCategoryTB)
    else:
        statement = select(MenuCategoryTB).where(
            MenuCategoryTB.user_id == user_id,
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
                name=menu_category.name,
                description=menu_category.description,
                image=menu_category.image,
            )
        )
    return menu_categories_list


async def get_menu_category(menu_category_id: int) -> MenuCategory:
    statement = select(MenuCategoryTB).where(MenuCategoryTB.id == menu_category_id)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    menu_category = query.scalars().first()
    return MenuCategory(
        id=menu_category.id,
        name=menu_category.name,
        description=menu_category.description,
        image=menu_category.image,
    )


async def insert_menu_category(user_id: int, menu_category: MenuCategory) -> None:
    statement = insert(MenuCategoryTB).values(
        user_id=user_id,
        name=menu_category.name,
        description=menu_category.description,
        image=menu_category.image,
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def update_menu_category(
    user_id: int, menu_category: MenuCategory
) -> MenuCategory:
    statement = (
        update(MenuCategoryTB)
        .where(MenuCategoryTB.id == menu_category.id, MenuCategoryTB.user_id == user_id)
        .values(
            name=menu_category.name,
            description=menu_category.description,
            image=menu_category.image,
        )
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return menu_category


async def delete_menu_category(user_id: int, menu_category_id: int) -> None:
    statement = delete(MenuCategoryTB).where(
        MenuCategoryTB.id == menu_category_id, MenuCategoryTB.user_id == user_id
    )
    try:
        await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return None


async def get_menu_items(user_id: int, menu_id: Optional[int] = None) -> List[MenuItem]:
    if menu_id is None:
        statement = (
            select(
                MenuItemTB.id,
                MenuItemTB.name,
                MenuItemTB.description,
                MenuItemTB.price,
                MenuItemTB.making_time,
                MenuItemTB.image,
                MenuItemTB.status,
                MenuItemTB.spice_level,
                MenuItemTB.vegetarian,
                MenuItemTB.vegan,
                MenuItemTB.gluten_free,
                MenuCategoryTB.name.label("menu_category_name"),
            )
            .where(MenuItemTB.user_id == user_id)
            .join(MenuCategoryTB)
        )
    else:
        statement = (
            select(
                MenuItemTB.id,
                MenuItemTB.name,
                MenuItemTB.description,
                MenuItemTB.price,
                MenuItemTB.making_time,
                MenuItemTB.image,
                MenuItemTB.status,
                MenuItemTB.spice_level,
                MenuItemTB.vegetarian,
                MenuItemTB.vegan,
                MenuItemTB.gluten_free,
                MenuCategoryTB.name.label("menu_category_name"),
            )
            .where(MenuItemTB.id == menu_id, MenuItemTB.user_id == user_id)
            .join(MenuCategoryTB)
        )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception as e:
        print(e)
        raise DatabaseQueryException
    menu_items = query.fetchall()
    menu_items_list = []
    for menu_item in menu_items:
        menu_items_list.append(
            MenuItem(
                id=menu_item.id,
                menu_category_name=menu_item.menu_category_name,
                name=menu_item.name,
                description=menu_item.description,
                price=menu_item.price,
                making_time=menu_item.making_time,
                image=menu_item.image,
                status=menu_item.status,
                spice_level=menu_item.spice_level,
                vegetarian=menu_item.vegetarian,
                vegan=menu_item.vegan,
                gluten_free=menu_item.gluten_free,
            )
        )
    return menu_items_list


async def insert_menu_item(user_id: int, menu_item: MenuItem) -> None:
    statement = insert(MenuItemTB).values(
        user_id=user_id,
        menu_category_id=menu_item.menu_category_id,
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        making_time=menu_item.making_time,
        image=menu_item.image,
        status=menu_item.status,
        spice_level=menu_item.spice_level,
        vegetarian=menu_item.vegetarian,
        vegan=menu_item.vegan,
        gluten_free=menu_item.gluten_free,
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception as e:
        print(e)
        raise DatabaseInsertException
    return None


async def update_menu_item(user_id: int, menu_item: MenuItem) -> MenuItem:
    statement = (
        update(MenuItemTB)
        .where(MenuItemTB.id == menu_item.id, MenuItemTB.user_id == user_id)
        .values(
            menu_category_id=menu_item.menu_category_id,
            name=menu_item.name,
            description=menu_item.description,
            price=menu_item.price,
            making_time=menu_item.making_time,
            image=menu_item.image,
            status=menu_item.status,
            spice_level=menu_item.spice_level,
            vegetarian=menu_item.vegetarian,
            vegan=menu_item.vegan,
            gluten_free=menu_item.gluten_free,
        )
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    return menu_item


async def delete_menu_item(user_id: int, menu_id: int) -> None:
    statement = delete(MenuItemTB).where(
        MenuItemTB.id == menu_id, MenuItemTB.user_id == user_id
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
