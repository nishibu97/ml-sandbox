from fastapi import FastAPI

from app.features.health.router import router as health_router
from app.features.items.router import router as items_router

app = FastAPI(title="api", version="0.1.0")

app.include_router(health_router)
app.include_router(items_router)
