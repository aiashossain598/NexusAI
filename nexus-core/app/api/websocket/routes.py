from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.send(f"Nexus: {message}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)