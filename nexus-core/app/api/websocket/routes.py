"""WebSocket streaming routes for real-time Nexus AI interaction."""

from __future__ import annotations

import json
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.websocket.manager import manager
from app.core.registry import registry
from app.memory.manager import memory_manager

router = APIRouter()


@router.websocket("/ws")
@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)

    # Send welcome / status handshake
    await websocket.send_json({
        "type": "connected",
        "service": "Nexus AI Core",
        "status": "ready",
    })

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
            except Exception:
                data = {"type": "chat", "instruction": raw_data}

            msg_type = data.get("type", "chat")

            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if msg_type == "confirm":
                confirm_id = data.get("confirmation_id")
                approved = data.get("approved", True)
                confirmations = registry.get("confirmation_manager")
                if confirmations and confirm_id:
                    if approved:
                        success = confirmations.approve(confirm_id)
                        await websocket.send_json({"type": "confirm_result", "confirmation_id": confirm_id, "status": "approved" if success else "not_found"})
                    else:
                        confirmations.reject(confirm_id)
                        await websocket.send_json({"type": "confirm_result", "confirmation_id": confirm_id, "status": "rejected"})
                continue

            if msg_type == "chat":
                instruction = data.get("instruction", "").strip()
                session_id = data.get("session_id", "desktop")

                if not instruction:
                    await websocket.send_json({"type": "error", "content": "Instruction cannot be empty."})
                    continue

                memory_manager.add_message(session_id, "user", instruction)

                factory = registry.get("coding_agent_factory")
                if not factory:
                    await websocket.send_json({"type": "error", "content": "Agent runtime is not ready."})
                    continue

                agent = factory()
                collected_text: list[str] = []

                for step in agent.run(instruction):
                    await websocket.send_json(step)
                    if step.get("type") == "text":
                        collected_text.append(step.get("content", ""))

                full_reply = " ".join(collected_text) if collected_text else "Task completed."
                memory_manager.add_message(session_id, "assistant", full_reply)

    except WebSocketDisconnect:
        manager.disconnect(websocket)