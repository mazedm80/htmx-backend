from typing import Optional, List

from fastapi import APIRouter, Depends

from api.order.schemas import Order, OrderDetail, OrderStatus
from api.order.services import (
    fetch_orders,
    fetch_order,
    create_order,
    update_order,
    remove_order,
    fetch_order_details,
    create_order_detail,
    remove_order_details,
    fetch_orders_by_status,
)
from core.auth.models import AuthGroup, Permission, TokenData
from core.auth.services import PermissionChecker
from core.base.error import UnauthorizedException

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get("")
async def get_orders(
    restaurant_id: int,
    hours: Optional[int] = None,
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
) -> List[Order]:
    if authorize.user_id:
        orders = await fetch_orders(restaurant_id=restaurant_id, hours=hours)
        return orders
    raise UnauthorizedException


@router.get("/by_status")
async def get_orders_by_status(
    restaurant_id: int,
    status: OrderStatus,
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
) -> List[Order]:
    if authorize.user_id:
        orders = await fetch_orders_by_status(
            restaurant_id=restaurant_id, status=status
        )
        return orders
    raise UnauthorizedException


@router.get("/details")
async def get_order(
    order_id: str,
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
) -> Order:
    if authorize.user_id:
        order = await fetch_order(order_id=order_id)
        return order
    raise UnauthorizedException


@router.post("")
async def post_order(
    restaurant_id: int,
    order: Order,
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
) -> str:
    if authorize.user_id:
        order_id = await create_order(restaurant_id=restaurant_id, order=order)
        return order_id
    raise UnauthorizedException


@router.put("")
async def put_order(
    order_id: str,
    order: Order,
    order_details: Optional[List[OrderDetail]],
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
        await update_order(order_id=order_id, order=order)
        if order_details is not None:
            await remove_order_details(order_id=order_id)
            try:
                for order_detail in order_details:
                    await create_order_detail(
                        order_id=order_id, order_detail=order_detail
                    )
            except Exception as e:
                print(e)
        return None
    raise UnauthorizedException


@router.delete("")
async def delete_order(
    order_id: str,
    authorize: TokenData = Depends(
        PermissionChecker(
            Permission(
                groups=[
                    AuthGroup.SUPER_ADMIN,
                    AuthGroup.ADMIN,
                    AuthGroup.OWNER,
                ]
            )
        )
    ),
) -> None:
    if authorize.user_id:
        await remove_order(order_id=order_id)
        await remove_order_details(order_id=order_id)
        return None
    raise UnauthorizedException


@router.get("/order_details")
async def get_order_details(
    order_id: str,
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
) -> List[OrderDetail]:
    if authorize.user_id:
        order_details = await fetch_order_details(order_id=order_id)
        return order_details
    raise UnauthorizedException


@router.post("/order_details")
async def post_order_detail(
    order_id: str,
    order_detail: List[OrderDetail],
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
        for detail in order_detail:
            await create_order_detail(order_id=order_id, order_detail=detail)
        return None
    raise UnauthorizedException
