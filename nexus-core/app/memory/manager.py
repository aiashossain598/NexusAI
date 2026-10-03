"""High-level Memory Manager for Nexus AI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.memory.models import ChatMessage, MemoryCategory, MemoryItem
from app.memory.store import MemoryStore


class MemoryManager:
    """Coordinates working memory, episodic conversation history, and semantic memory."""

    def __init__(self, storage_path: Path | str | None = None) -> None:
        self.store = MemoryStore(storage_path)
        self._conversations: dict[str, list[ChatMessage]] = {}

    def remember(
        self,
        key: str,
        content: str,
        category: MemoryCategory = MemoryCategory.WORKING,
        importance: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryItem:
        item = MemoryItem(
            key=key,
            content=content,
            category=category,
            importance=importance,
            metadata=metadata or {},
        )
        self.store.store(item)
        return item

    def recall(
        self,
        query: str,
        category: MemoryCategory | None = None,
        limit: int = 5,
    ) -> list[MemoryItem]:
        return self.store.search(query, category=category, limit=limit)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        tool_calls: list[dict[str, Any]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ChatMessage:
        if session_id not in self._conversations:
            self._conversations[session_id] = []
        msg = ChatMessage(
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            metadata=metadata or {},
        )
        self._conversations[session_id].append(msg)
        return msg

    def get_messages(self, session_id: str, limit: int = 50) -> list[ChatMessage]:
        messages = self._conversations.get(session_id, [])
        return messages[-limit:]

    def clear_conversation(self, session_id: str) -> None:
        if session_id in self._conversations:
            del self._conversations[session_id]

    def build_context_prompt(self, query: str, session_id: str | None = None) -> str:
        """Assembles relevant memories and past interactions into a context block."""
        parts: list[str] = []

        memories = self.recall(query, limit=3)
        if memories:
            parts.append("### Relevant Memory Context:")
            for m in memories:
                parts.append(f"- [{m.category.value}] {m.key}: {m.content}")

        if session_id and session_id in self._conversations:
            recent = self.get_messages(session_id, limit=5)
            if recent:
                parts.append("### Recent Conversation:")
                for r in recent:
                    parts.append(f"{r.role}: {r.content}")

        return "\n".join(parts)


memory_manager = MemoryManager()
