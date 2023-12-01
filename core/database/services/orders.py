from typing import List, Optional

from sqlalchemy import delete, select, update, func
from sqlalchemy.dialects.postgresql import insert

from api.order.schemas import Order, OrderDetail, OrderStatus, PaymentStatus
from core.base.error import DatabaseInsertException, DatabaseQueryException
from core.database.orm.menus import MenuItemTB
from core.database.orm.orders import OrderTB, OrderDetailTB
from core.database.postgres import PSQLHandler


async def get_orders(restaurant_id: int, hours: Optional[int] = None) -> List[Order]:
    if hours is None:
        statement = (
            select(OrderTB)
            .where(
                OrderTB.restaurant_id == restaurant_id,
            )
            .where(
                OrderTB.created_at
                >= func.now()
                - func.make_interval(
                    0, 0, 0, 0, 24
                ),  # years, months, weeks, days, hours
            )
        )

    else:
        statement = select(OrderTB).where(
            OrderTB.restaurant_id == restaurant_id,
            OrderTB.created_at
            >= func.now()
            - func.make_interval(
                0, 0, 0, 0, hours
            ),  # years, months, weeks, days, hours
        )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    orders = query.scalars().all()
    orders_list = []
    for order in orders:
        orders_list.append(
            Order(
                order_id=order.order_id,
                restaurant_id=order.restaurant_id,
                table_number=order.table_number,
                status=order.status,
                order_type=order.order_type,
                payment_status=order.payment_status,
                total_amount=order.total_amount,
                coupon_code=order.coupon_code,
                time=order.updated_at,
            )
        )
    return orders_list


async def get_orders_by_status(
    restaurant_id: int, status: OrderStatus, payment_status: PaymentStatus
) -> List[Order]:
    if status:
        statement = select(OrderTB).where(
            OrderTB.restaurant_id == restaurant_id,
            OrderTB.status == status,
            OrderTB.created_at
            >= func.now()
            - func.make_interval(
                0, 0, 0, 20, 24
            ),  # years, months, weeks, days, hours (20 days)
        )
    elif payment_status:
        statement = select(OrderTB).where(
            OrderTB.restaurant_id == restaurant_id,
            OrderTB.payment_status == payment_status,
            OrderTB.created_at
            >= func.now()
            - func.make_interval(
                0, 0, 0, 20, 24
            ),  # years, months, weeks, days, hours (20 days)
        )
    else:
        raise DatabaseQueryException
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception as e:
        print(e)
        raise DatabaseQueryException
    orders = query.scalars().all()
    orders_list = []
    for order in orders:
        orders_list.append(
            Order(
                order_id=order.order_id,
                restaurant_id=order.restaurant_id,
                table_number=order.table_number,
                status=order.status,
                order_type=order.order_type,
                payment_status=order.payment_status,
                total_amount=order.total_amount,
                coupon_code=order.coupon_code,
                time=order.updated_at,
            )
        )
    return orders_list


async def get_order(order_id: str) -> Order:
    statement = select(OrderTB).where(OrderTB.order_id == order_id)
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    order = query.scalars().first()
    return Order(
        order_id=order.order_id,
        restaurant_id=order.restaurant_id,
        table_number=order.table_number,
        status=order.status,
        order_type=order.order_type,
        payment_status=order.payment_status,
        total_amount=order.total_amount,
        coupon_code=order.coupon_code,
        time=order.updated_at,
    )


async def insert_order(restaurant_id: int, order: Order) -> str:
    statement = insert(OrderTB).values(
        order_id=order.order_id,
        restaurant_id=restaurant_id,
        table_number=order.table_number,
        status=order.status,
        order_type=order.order_type,
        payment_status=order.payment_status,
        total_amount=order.total_amount,
        coupon_code=order.coupon_code,
    )
    try:
        response = await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
    if response is None:
        raise DatabaseInsertException
    return response.inserted_primary_key[0]


async def update_order(order: Order) -> None:
    statement = (
        update(OrderTB)
        .where(OrderTB.order_id == order.order_id)
        .values(
            status=order.status,
            order_type=order.order_type,
            payment_status=order.payment_status,
            total_amount=order.total_amount,
            coupon_code=order.coupon_code,
            updated_at=func.now(),
        )
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException


async def update_order_status(
    order_id: str,
    status: Optional[OrderStatus] = None,
    payment_status: Optional[OrderStatus] = None,
) -> None:
    statement = update(OrderTB).where(OrderTB.order_id == order_id)
    if status is not None:
        statement = statement.values(status=status)
    if payment_status is not None:
        statement = statement.values(payment_status=payment_status)
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException


async def delete_order(order_id: str) -> None:
    statement = delete(OrderTB).where(OrderTB.order_id == order_id)
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException


async def get_order_details(order_id: str) -> List[OrderDetail]:
    statement = (
        select(
            OrderDetailTB.order_id,
            OrderDetailTB.menu_item_id,
            MenuItemTB.name,
            OrderDetailTB.quantity,
            OrderDetailTB.price,
        )
        .join(MenuItemTB, OrderDetailTB.menu_item_id == MenuItemTB.id)
        .where(OrderDetailTB.order_id == order_id)
    )
    try:
        query = await PSQLHandler().execute(statement=statement)
    except Exception:
        raise DatabaseQueryException
    order_details = query.fetchall()
    order_details_list = []
    for order_detail in order_details:
        order_details_list.append(
            OrderDetail(
                order_id=order_detail.order_id,
                menu_item_id=order_detail.menu_item_id,
                name=order_detail.name,
                quantity=order_detail.quantity,
                price=order_detail.price,
            )
        )
    return order_details_list


async def insert_order_detail(order_id: str, order_detail: OrderDetail) -> None:
    statement = insert(OrderDetailTB).values(
        order_id=order_id,
        menu_item_id=order_detail.menu_item_id,
        quantity=order_detail.quantity,
        price=order_detail.price,
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException


async def delete_order_details(order_id: str) -> None:
    statement = delete(OrderDetailTB).where(OrderDetailTB.order_id == order_id)
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise DatabaseInsertException
