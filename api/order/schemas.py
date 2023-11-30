from datetime import datetime

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"


class OrderType(str, Enum):
    dine_in = "dine_in"
    take_away = "take_away"
    delivery = "delivery"


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Order(BaseModel):
    order_id: str = Field(description="Order ID")
    user_id: Optional[int] = Field(default=None, description="User ID")
    table_number: Optional[int] = Field(default=None, description="Table Number")
    status: OrderStatus = Field(description="Order Status")
    order_type: OrderType = Field(description="Order Type")
    payment_status: PaymentStatus = Field(description="Payment Status")
    total_amount: float = Field(description="Total Amount")
    coupon_code: Optional[str] = Field(default=None, title="Coupon Code")
    note: Optional[str] = Field(default=None, title="Note")
    time: Optional[datetime] = Field(default=None, description="Time")


class OrderDetail(BaseModel):
    order_id: Optional[str] = Field(default=None, description="Order ID")
    menu_item_id: int = Field(description="Menu Item ID")
    name: Optional[str] = Field(default=None, description="Name of the menu item")
    quantity: int = Field(description="Quantity")
    price: float = Field(description="Price")
