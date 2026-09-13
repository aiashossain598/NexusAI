from fastapi import FastAPI

from app.api.routes.system import router as system_router

app = FastAPI(
    title="Nexus AI Core",
    version="0.1.0",
)

app.include_router(system_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Nexus AI Core",
    }