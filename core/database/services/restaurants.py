from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from api.restaurant.schemas import Restaurant
from core.database import PSQLHandler
from core.database.orm.restaurants import RestaurantTB, RestaurantAccessTB
from core.database.orm.users import User


async def get_all_restaurants():
    statement = select(RestaurantTB)
    try:
        query = await PSQLHandler().scalars(statement=statement)
    except Exception:
        print("Error while executing query")
    restaurants = query.fetchall()
    return restaurants


async def insert_restaurant(restaurant: Restaurant, email: str) -> None:
    owner_id = select(User.id).where(User.email == email)
    query = await PSQLHandler().execute(statement=owner_id)
    owner_id = query.fetchone()[0]
    statement = insert(RestaurantTB).values(
        owner_id=owner_id,
        name=restaurant.name,
        address=restaurant.address,
        phone=restaurant.phone,
        email=restaurant.email,
        website=restaurant.website,
        image=restaurant.image,
    )
    try:
        await PSQLHandler().execute_commit(statement=statement)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while creating restaurant",
            headers={"WWW-Authenticate": "Bearer"},
        )
