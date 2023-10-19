from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    id: int
    name: str
    description: str
    address: str
    phone_number: str
    email: str
    website: str
    image: str
    latitude: float
    longitude: float
    created_at: str
    updated_at: str
