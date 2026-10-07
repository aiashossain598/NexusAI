"""API Key authentication middleware for Nexus AI."""

from __future__ import annotations

import os

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Routes that are always public (health + root)
_PUBLIC_PATHS: frozenset[str] = frozenset({"/", "/health", "/docs", "/openapi.json", "/redoc"})


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Enforces X-API-Key header when NEXUS_API_KEY is configured.

    If the environment variable is not set the middleware is a no-op,
    allowing frictionless local development without credentials.
    """

    def __init__(self, app, *, env_var: str = "NEXUS_API_KEY") -> None:
        super().__init__(app)
        self._api_key: str | None = os.getenv(env_var)

    async def dispatch(self, request: Request, call_next) -> Response:
        # No key configured -> auth disabled (dev mode)
        if not self._api_key:
            return await call_next(request)

        # Always allow public / health paths
        if request.url.path in _PUBLIC_PATHS:
            return await call_next(request)

        # WebSocket upgrade - check query param or header
        provided = (
            request.headers.get("X-API-Key")
            or request.query_params.get("api_key")
        )

        if provided != self._api_key:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid or missing API key. Supply X-API-Key header.",
                    "status": "unauthorized",
                },
            )

        return await call_next(request)
