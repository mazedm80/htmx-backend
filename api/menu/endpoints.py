from fastapi import APIRouter, Depends

from api.menu.schemas import MenuCategory, MenuCategoryList, MenuItem, MenuItemList
from api.menu.services import (
    create_menu_category,
    create_menu_item,
    fetch_menu_categories,
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


@router.get("/{restaurant_id}")
async def get_menu_items(
    restaurant_id: int,
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
            restaurant_id=restaurant_id,
        )
        return MenuItemList(menu_items=menu_items)
    raise UnauthorizedException


@router.post("/{restaurant_id}")
async def post_menu_item(
    restaurant_id: int,
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
            restaurant_id=restaurant_id,
            menu_item=menu_item,
        )
        return None
    raise UnauthorizedException


@router.put("/{restaurant_id}")
async def put_menu_item(
    restaurant_id: int,
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
        await modify_menu_item(
            user_id=authorize.user_id,
            restaurant_id=restaurant_id,
            menu_item=menu_item,
        )
        return None
    raise UnauthorizedException


@router.delete("/{restaurant_id}")
async def delete_menu_item(
    restaurant_id: int,
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
        await remove_menu_item(
            user_id=authorize.user_id,
            restaurant_id=restaurant_id,
        )
        return None
    raise UnauthorizedException


@router.get("categories/")
async def get_menu_categories() -> MenuCategoryList:
    menu_categories = await fetch_menu_categories(
        user_id=None,
        restaurant_id=None,
    )
    return MenuCategoryList(menu_categories=menu_categories)


@router.get("categories/{restaurant_id}")
async def get_menu_categories(
    restaurant_id: int,
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
) -> MenuCategoryList:
    if authorize.user_id:
        menu_categories = await fetch_menu_categories(
            user_id=authorize.user_id,
            restaurant_id=restaurant_id,
        )
        return MenuCategoryList(menu_categories=menu_categories)
    raise UnauthorizedException


@router.post("categories/{restaurant_id}")
async def post_menu_category(
    restaurant_id: int,
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
            restaurant_id=restaurant_id,
            menu_category=menu_category,
        )
        return None
    raise UnauthorizedException


@router.put("categories/{restaurant_id}")
async def put_menu_category(
    restaurant_id: int,
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
            restaurant_id=restaurant_id,
            menu_category=menu_category,
        )
        return None
    raise UnauthorizedException


@router.delete("categories/{restaurant_id}/{menu_category_id}")
async def delete_menu_category(
    restaurant_id: int,
    menu_category_id: int,
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
            restaurant_id=restaurant_id,
            menu_category_id=menu_category_id,
        )
        return None
    raise UnauthorizedException
