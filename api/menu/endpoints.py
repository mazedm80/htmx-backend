from typing import Optional

from fastapi import APIRouter, Depends

from api.menu.schemas import MenuCategory, MenuCategoryList, MenuItem, MenuItemList
from api.menu.services import (
    create_menu_category,
    create_menu_item,
    fetch_menu_categories,
    fetch_menu_category,
    fetch_menu_items,
    modify_menu_category,
    modify_menu_item,
    remove_menu_category,
    remove_menu_item,
)
from core.auth.models import AuthGroup, Permission, TokenData
from core.auth.services import PermissionChecker
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
)


@router.get("")
async def get_menu_items(
    menu_id: Optional[int] = None,
    category_id: Optional[int] = None,
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
) -> MenuItemList:
    if authorize.user_id:
        menu_items = await fetch_menu_items(
            user_id=authorize.user_id,
            menu_id=menu_id,
            category_id=category_id,
        )
        return MenuItemList(menu_items=menu_items)
    raise UnauthorizedException


@router.post("")
async def post_menu_item(
    menu_item: MenuItem,
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
) -> None:
    if authorize.user_id:
        await create_menu_item(
            user_id=authorize.user_id,
            menu_item=menu_item,
        )
        return None
    raise UnauthorizedException


@router.put("")
async def put_menu_item(
    menu_item: MenuItem,
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
) -> None:
    if authorize.user_id:
        try:
            await modify_menu_item(
                user_id=authorize.user_id,
                menu_item=menu_item,
            )
        except Exception as e:
            print(e)
        return None
    raise UnauthorizedException


@router.delete("")
async def delete_menu_item(
    menu_id: int,
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
) -> None:
    if authorize.user_id and menu_id:
        await remove_menu_item(
            user_id=authorize.user_id,
            menu_id=menu_id,
        )
        return None
    raise UnauthorizedException


@router.get("/categories")
async def get_menu_categories() -> MenuCategoryList:
    menu_categories = await fetch_menu_categories(user_id=None)
    return MenuCategoryList(menu_categories=menu_categories)


@router.get("/category")
async def get_menu_category(
    category_id: Optional[int],
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
) -> MenuCategory:
    if authorize.user_id:
        menu_category = await fetch_menu_category(category_id=category_id)
        return menu_category
    raise UnauthorizedException


@router.post("/category")
async def post_menu_category(
    menu_category: MenuCategory,
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
) -> None:
    if authorize.user_id:
        await create_menu_category(
            user_id=authorize.user_id,
            menu_category=menu_category,
        )
        return None
    raise UnauthorizedException


@router.put("/category")
async def put_menu_category(
    menu_category: MenuCategory,
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
) -> None:
    if authorize.user_id:
        await modify_menu_category(
            user_id=authorize.user_id,
            menu_category=menu_category,
        )
        return None
    raise UnauthorizedException


@router.delete("/category")
async def delete_menu_category(
    category_id: int,
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
) -> None:
    if authorize.user_id:
        await remove_menu_category(
            user_id=authorize.user_id,
            category_id=category_id,
        )
        return None
    raise UnauthorizedException
