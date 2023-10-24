from typing import List, Optional

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    """Restaurant model"""

    id: int = Field(
        description="Id of the restaurant. It is not required for creation.",
        default=None,
    )
    name: str = Field(
        description="Name of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    address: str = Field(
        description="Address of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    phone: str = Field(
        description="Phone of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    email: str = Field(
        description="Email of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    website: str = Field(
        description="Website of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )
    image: str = Field(
        description="Image of the restaurant. It must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
    )


class RestaurantsList(BaseModel):
    """RestaurantsList model"""

    restaurants: List[Restaurant]


class RestaurantAccess(BaseModel):
    """RestaurantAccess model"""

    user_id: int
    restaurant_id: int
