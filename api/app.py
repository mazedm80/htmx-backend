from api.auth.endpoints import router as auth_router
from fastapi import Depends, FastAPI

app = FastAPI(
    title="py-htmx test",
    description="py-htmx test",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
)

app.include_router(auth_router)
