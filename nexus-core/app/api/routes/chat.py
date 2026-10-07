"""Chat and Agent API routes for Nexus AI."""

from __future__ import annotations

import json
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.registry import registry
from app.memory.manager import memory_manager

router = APIRouter(prefix="/api/chat", tags=["Chat & Agent"])


class ChatRequest(BaseModel):
    instruction: str = Field(..., min_length=1, description="Instruction or prompt for Nexus AI")
    session_id: str = Field(default="default", description="Conversation session ID")
    confirmation_id: str | None = Field(default=None, description="Confirmation ID if approving a pending action")


class ConfirmationRequest(BaseModel):
    confirmation_id: str
    approved: bool = True


@router.post("")
@router.post("/")
async def chat_endpoint(request: ChatRequest) -> dict[str, Any]:
    instruction = request.instruction.strip()
    session_id = request.session_id

    # Add user message to memory
    memory_manager.add_message(session_id, "user", instruction)

    factory = registry.get("coding_agent_factory")
    if not factory:
        raise HTTPException(status_code=500, detail="Coding agent factory not registered in runtime.")

    # Check if this request is approving a pending confirmation
    if request.confirmation_id:
        confirmations = registry.get("confirmation_manager")
        if confirmations:
            confirmations.approve(request.confirmation_id)

    agent = factory()
    events: list[dict[str, Any]] = []
    text_pieces: list[str] = []
    pending_confirmation_id: str | None = None
    status = "completed"

    for step in agent.run(instruction):
        events.append(step)
        step_type = step.get("type")
        if step_type == "text":
            text_pieces.append(step.get("content", ""))
        elif step_type == "tool_result":
            content = step.get("content", {})
            if isinstance(content, dict) and content.get("status") == "confirmation_required":
                pending_confirmation_id = content.get("confirmation_id")
                status = "confirmation_required"
        elif step_type == "error":
            status = "error"
            text_pieces.append(step.get("content", ""))

    response_text = " ".join(text_pieces) if text_pieces else "Action completed."

    # Record assistant reply in memory
    memory_manager.add_message(
        session_id,
        "assistant",
        response_text,
        tool_calls=[e for e in events if e.get("type") == "tool_call"],
    )

    return {
        "response": response_text,
        "status": status,
        "session_id": session_id,
        "events": events,
        "confirmation_id": pending_confirmation_id,
    }


@router.post("/confirm")
async def confirm_action(request: ConfirmationRequest) -> dict[str, Any]:
    confirmations = registry.get("confirmation_manager")
    if not confirmations:
        raise HTTPException(status_code=500, detail="Confirmation manager not available.")

    if request.approved:
        success = confirmations.approve(request.confirmation_id)
        return {"status": "approved" if success else "not_found", "confirmation_id": request.confirmation_id}
    else:
        confirmations.reject(request.confirmation_id)
        return {"status": "rejected", "confirmation_id": request.confirmation_id}


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str) -> dict[str, Any]:
    messages = memory_manager.get_messages(session_id)
    return {
        "session_id": session_id,
        "messages": [m.to_dict() for m in messages],
    }
