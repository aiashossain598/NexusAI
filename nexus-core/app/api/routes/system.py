from fastapi import APIRouter

from app.services.system_service import SystemService

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/")
async def system():

    return SystemService.get_system_info()