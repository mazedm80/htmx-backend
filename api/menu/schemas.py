from typing import List, Optional

from pydantic import BaseModel, Field


class MenuCategory(BaseModel):
    """Menu Category model."""

    id: Optional[int] = Field(
        description="Menu Category ID. It is not required for creation.",
    )
    restaurant_id: int = Field(
        description="Restaurant ID",
    )
    name: str = Field(
        description="Name of the menu categor", min_length=3, max_length=50
    )


class MenuCategoryList(BaseModel):
    """Menu Category List model."""

    menu_categories: List[MenuCategory]


class MenuItem(BaseModel):
    """Menu Item model."""

    id: Optional[int] = Field(
        description="Menu Item ID. It is not required for creation.",
    )
    restaurant_id: int = Field(
        description="Restaurant ID",
    )
    menu_category_id: int = Field(
        description="Menu Category ID",
    )
    name: str = Field(description="Name of the menu item", min_length=3, max_length=50)
    description: str = Field(
        description="Description of the menu item", min_length=3, max_length=50
    )
    price: float = Field(
        description="Price of the menu item",
    )
    vegetarian: bool = Field(
        description="Is the menu item vegetarian",
    )
    vegan: bool = Field(
        description="Is the menu item vegan",
    )
    gluten_free: bool = Field(
        description="Is the menu item gluten free",
    )
    spicy: bool = Field(
        description="Is the menu item spicy",
    )


class MenuItemList(BaseModel):
    """Menu Item List model."""

    menu_items: List[MenuItem]
