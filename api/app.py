from fastapi import FastAPI

from api.auth.endpoints import router as auth_router
from api.menu.endpoints import router as menu_router
from api.restaurant.endpoints import router as restaurant_router
from api.order.endpoints import router as order_router

app = FastAPI(
    title="py-htmx test",
    description="py-htmx test",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
)

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(restaurant_router)
app.include_router(order_router)
