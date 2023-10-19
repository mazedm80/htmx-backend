from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.restaurant.schemas import Restaurant, RestaurantsList
from core.database.services.restaurants import get_all_restaurants, insert_restaurant


async def get_restaurant() -> List[Restaurant]:
    restaurants = await get_all_restaurants()
    restaurants_list = []
    for restaurant in restaurants:
        restaurants_list.append(
            Restaurant(
                name=restaurant.name,
                address=restaurant.address,
                phone=restaurant.phone,
                email=restaurant.email,
                website=restaurant.website,
                image=restaurant.image,
            )
        )
    return restaurants_list


async def create_restaurant(restaurant: Restaurant, email: str) -> None:
    restaurant = await insert_restaurant(restaurant=restaurant, email=email)
