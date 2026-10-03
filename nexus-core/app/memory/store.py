"""Memory storage engine for Nexus AI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.memory.models import MemoryCategory, MemoryItem


class MemoryStore:
    """Manages memory persistence with in-memory cache and optional JSON file storage."""

    def __init__(self, storage_path: Path | str | None = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else None
        self._items: dict[str, MemoryItem] = {}
        if self.storage_path and self.storage_path.exists():
            self.load()

    def store(self, item: MemoryItem) -> None:
        self._items[item.id] = item
        if self.storage_path:
            self.persist()

    def get(self, item_id: str) -> MemoryItem | None:
        return self._items.get(item_id)

    def find_by_key(self, key: str) -> list[MemoryItem]:
        return [item for item in self._items.values() if item.key == key]

    def list_by_category(self, category: MemoryCategory) -> list[MemoryItem]:
        return [item for item in self._items.values() if item.category == category]

    def search(self, query: str, category: MemoryCategory | None = None, limit: int = 10) -> list[MemoryItem]:
        query_lower = query.lower()
        results: list[tuple[float, MemoryItem]] = []

        for item in self._items.values():
            if category and item.category != category:
                continue
            relevance = 0.0
            if query_lower in item.key.lower():
                relevance += 2.0
            if query_lower in item.content.lower():
                relevance += 1.0
            if relevance > 0.0:
                results.append((relevance * item.importance, item))

        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:limit]]

    def delete(self, item_id: str) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            if self.storage_path:
                self.persist()
            return True
        return False

    def clear(self, category: MemoryCategory | None = None) -> None:
        if category is None:
            self._items.clear()
        else:
            self._items = {k: v for k, v in self._items.items() if v.category != category}
        if self.storage_path:
            self.persist()

    def count(self) -> int:
        return len(self._items)

    def persist(self) -> None:
        if not self.storage_path:
            return
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = [item.to_dict() for item in self._items.values()]
        self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.storage_path or not self.storage_path.exists():
            return
        try:
            raw = json.loads(self.storage_path.read_text(encoding="utf-8"))
            for entry in raw:
                item = MemoryItem(
                    id=entry.get("id", ""),
                    key=entry.get("key", ""),
                    content=entry.get("content", ""),
                    category=MemoryCategory(entry.get("category", MemoryCategory.WORKING.value)),
                    metadata=entry.get("metadata", {}),
                    importance=float(entry.get("importance", 1.0)),
                )
                self._items[item.id] = item
        except Exception:
            pass
