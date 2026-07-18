from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "Nexus AI",
        "version": "0.1.0",
    }