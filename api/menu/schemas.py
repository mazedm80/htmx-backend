from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SpiceLevel(str, Enum):
    """Spice Level Enum."""

    mild = "mild"
    medium = "medium"
    hot = "hot"
    extra = "extra"


class MenuCategory(BaseModel):
    """Menu Category model."""

    id: Optional[int] = Field(
        description="Menu Category ID. It is not required for creation.",
    )
    name: str = Field(
        description="Name of the menu categor", min_length=3, max_length=50
    )
    description: str = Field(
        description="Description of the menu category", min_length=3, max_length=250
    )
    image: str = Field(
        description="Image of the menu category",
    )


class MenuCategoryList(BaseModel):
    """Menu Category List model."""

    menu_categories: List[MenuCategory]


class MenuItem(BaseModel):
    """Menu Item model."""

    id: Optional[int] = Field(
        default=None,
        description="Menu Item ID. It is not required for creation.",
    )
    menu_category_id: Optional[int] = Field(
        default=None,
        description="Menu Category ID",
    )
    menu_category_name: Optional[str] = Field(
        default=None,
        description="Menu Category Name",
    )
    name: str = Field(description="Name of the menu item", min_length=3, max_length=200)
    description: str = Field(
        description="Description of the menu item", min_length=3, max_length=500
    )
    price: float = Field(
        description="Price of the menu item",
    )
    making_time: float = Field(
        description="Making time of the menu item",
    )
    image: str = Field(
        description="Image of the menu item",
    )
    status: bool = Field(
        description="Status of the menu item",
    )
    spice_level: SpiceLevel = Field(
        description="Spice level of the menu item",
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


class MenuItemList(BaseModel):
    """Menu Item List model."""

    menu_items: List[MenuItem]
