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


class MenuCategoryTB(Base):
    __tablename__ = "menu_categories"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=True)
    image = Column(TEXT, nullable=True)
    created_at = Column(DATETIME(timezone=True), server_default=func.now())
    updated_at = Column(DATETIME(timezone=True), server_default=func.now())


class MenuItemTB(Base):
    __tablename__ = "menu_items"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    menu_category_id = Column(
        INTEGER, ForeignKey("menu_categories.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(REAL, nullable=False)
    making_time = Column(REAL, nullable=True)
    image = Column(TEXT, nullable=True)
    status = Column(BOOLEAN, default=True)
    spice_level = Column(
        Enum("mild", "medium", "hot", "extra", name="spice_level", create_type=False),
        default="mild",
    )
    vegetarian = Column(BOOLEAN, default=False)
    vegan = Column(BOOLEAN, default=False)
    gluten_free = Column(BOOLEAN, default=False)
    created_at = Column(DATETIME(timezone=True), server_default=func.now())
    updated_at = Column(DATETIME(timezone=True), server_default=func.now())
