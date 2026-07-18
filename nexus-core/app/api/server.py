from fastapi import FastAPI
from app.api.routes.health import router
from app.api.websocket.routes import router as websocket_router

app = FastAPI(
    title="Nexus AI API",
    version="0.1.0",
)

app.include_router(router)
app.include_router(websocket_router)