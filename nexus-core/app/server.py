"""Unified FastAPI Server for Nexus AI."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.system import router as system_router
from app.api.websocket.routes import router as websocket_router
from app.core.bootstrap import Bootstrap


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Initialize core services, container, and registry on server boot
    Bootstrap().start()
    yield


app = FastAPI(
    title="Nexus AI Core API",
    description="Unified API & WebSocket gateway for Nexus AI",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for desktop, web, and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(health_router)
app.include_router(system_router)
app.include_router(chat_router)
app.include_router(websocket_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Nexus AI Core",
        "version": "0.1.0",
    }