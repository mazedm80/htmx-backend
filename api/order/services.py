from typing import List, Optional

from api.order.schemas import Order, OrderDetail, OrderStatus, PaymentStatus
from core.database.services.orders import (
    get_orders,
    get_order,
    insert_order,
    update_order,
    update_order_status,
    delete_order,
    get_order_details,
    insert_order_detail,
    delete_order_details,
    get_orders_by_status,
)


async def fetch_orders(restaurant_id: int, hours: Optional[int] = None) -> List[Order]:
    orders = await get_orders(restaurant_id=restaurant_id, hours=hours)
    return orders


async def fetch_orders_by_status(
    restaurant_id: int, status: OrderStatus, payment_status: PaymentStatus
) -> List[Order]:
    orders = await get_orders_by_status(
        restaurant_id=restaurant_id, status=status, payment_status=payment_status
    )
    return orders


async def fetch_order(order_id: str) -> Order:
    order = await get_order(order_id=order_id)
    return order


async def create_order(restaurant_id: int, order: Order) -> str:
    order_id = await insert_order(restaurant_id=restaurant_id, order=order)
    return order_id


async def modify_order(order_id: str, order: Order) -> None:
    await update_order(order_id=order_id, order=order)


async def modify_order_status(
    order_id: str,
    status: Optional[OrderStatus] = None,
    payment_status: Optional[OrderStatus] = None,
) -> None:
    await update_order_status(
        order_id=order_id, status=status, payment_status=payment_status
    )


async def remove_order(order_id: str) -> None:
    await delete_order(order_id=order_id)


async def fetch_order_details(order_id: str) -> List[OrderDetail]:
    order_details = await get_order_details(order_id=order_id)
    return order_details


async def create_order_detail(order_id: str, order_detail: OrderDetail) -> None:
    await insert_order_detail(order_id=order_id, order_detail=order_detail)


async def remove_order_details(order_id: str) -> None:
    await delete_order_details(order_id=order_id)
