"""Memory models for Nexus AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import uuid


class MemoryCategory(str, Enum):
    WORKING = "working"        # Active task, current scratchpad
    EPISODIC = "episodic"      # Conversational turns, past session events
    SEMANTIC = "semantic"      # Knowledge, facts, guidelines
    PREFERENCE = "preference"  # User preferences, project settings


@dataclass(slots=True)
class MemoryItem:
    key: str
    content: str
    category: MemoryCategory = MemoryCategory.WORKING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)
    importance: float = 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "key": self.key,
            "content": self.content,
            "category": self.category.value,
            "metadata": self.metadata,
            "importance": self.importance,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass(slots=True)
class ChatMessage:
    role: str
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "tool_calls": self.tool_calls,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }
