from typing import Any


class ServiceRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, Any] = {}

    def add(self, name: str, service: Any) -> None:
        self._registry[name] = service

    def get(self, name: str) -> Any:
        return self._registry.get(name)

    def remove(self, name: str) -> None:
        self._registry.pop(name, None)

    def all(self) -> dict[str, Any]:
        return self._registry.copy()


registry = ServiceRegistry()