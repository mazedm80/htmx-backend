from sqlalchemy import (
    BOOLEAN,
    DATETIME,
    INTEGER,
    REAL,
    TEXT,
    Column,
    Enum,
    ForeignKey,
    func,
)

from core.database import Base


class OrderTB(Base):
    __tablename__ = "orders"

    order_id = Column(TEXT, primary_key=True, index=True)
    user_id = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    restaurant_id = Column(
        INTEGER, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False
    )
    table_number = Column(INTEGER, nullable=False)
    status = Column(
        Enum(
            "pending",
            "accepted",
            "rejected",
            "cancelled",
            name="order_status",
            create_type=False,
        ),
        default="pending",
    )
    order_type = Column(
        Enum(
            "dine_in",
            "take_away",
            "delivery",
            name="order_type",
            create_type=False,
        ),
        default="dine_in",
    )
    payment_status = Column(
        Enum(
            "pending",
            "paid",
            "cancelled",
            name="payment_status",
            create_type=False,
        ),
        default="pending",
    )
    total_amount = Column(REAL, nullable=False)
    coupon_code = Column(TEXT, nullable=True)
    created_at = Column(DATETIME(timezone=True), server_default=func.now())
    updated_at = Column(DATETIME(timezone=True), server_default=func.now())


class OrderDetailTB(Base):
    __tablename__ = "order_details"

    id = Column(INTEGER, primary_key=True, index=True)
    order_id = Column(TEXT, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(
        INTEGER, ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(INTEGER, nullable=False)
    price = Column(REAL, nullable=False)
    created_at = Column(DATETIME(timezone=True), server_default=func.now())
    updated_at = Column(DATETIME(timezone=True), server_default=func.now())
