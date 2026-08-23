from fastapi import FastAPI

from app.features.deps.router import router as deps_router
from app.features.health.router import router as health_router
from app.features.users.router import router as users_router

app = FastAPI(title="api", version="0.1.0")

app.include_router(health_router)
app.include_router(deps_router)
app.include_router(users_router, prefix="/graphql")