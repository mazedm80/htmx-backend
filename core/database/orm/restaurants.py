from sqlalchemy import INTEGER, TEXT, Column, DateTime, ForeignKey, func

from core.database import Base


class RestaurantTB(Base):
    """Restaurant model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "restaurants"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    address = Column(TEXT, nullable=False)
    phone = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    website = Column(TEXT, nullable=True)
    image = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class RestaurantAccessTB(Base):
    """RestaurantAccess model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "restaurant_access"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(
        INTEGER, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False
    )
    restaurant_id = Column(
        INTEGER, ForeignKey("public.restaurants.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class RestaurantTableTB(Base):
    """RestaurantTable model"""

    __table_args__ = {"schema": "public"}
    __tablename__ = "restaurant_tables"

    id = Column(INTEGER, autoincrement=True)
    restaurant_id = Column(
        INTEGER,
        ForeignKey("public.restaurants.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    table_number = Column(INTEGER, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
