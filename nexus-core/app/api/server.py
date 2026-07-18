from fastapi import FastAPI
from app.api.routes.health import router

app = FastAPI(
    title="Nexus AI API",
    version="0.1.0",
)

app.include_router(router)