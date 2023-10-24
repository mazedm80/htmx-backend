from sqlalchemy import INTEGER, TEXT, Column, DateTime, ForeignKey, func

from core.database import Base


class MenuCategoryTB(Base):
    __tablename__ = "menu_categories"

    id = Column(INTEGER, primary_key=True, index=True)
    restaurant_id = Column(
        INTEGER, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(TEXT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class MenuItemTB(Base):
    __tablename__ = "menu_items"

    id = Column(INTEGER, primary_key=True, index=True)
    restaurant_id = Column(
        INTEGER, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False
    )
    menu_category_id = Column(
        INTEGER, ForeignKey("menu_categories.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    price = Column(INTEGER, nullable=False)
    vegetarian = Column(INTEGER, nullable=False)
    vegan = Column(INTEGER, nullable=False)
    gluten_free = Column(INTEGER, nullable=False)
    spicy = Column(INTEGER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
