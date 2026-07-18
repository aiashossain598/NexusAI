from typing import Any


class ServiceContainer:
    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        if name in self._services:
            raise ValueError(f"Service '{name}' already registered.")
        self._services[name] = service

    def get(self, name: str) -> Any:
        if name not in self._services:
            raise KeyError(f"Service '{name}' not found.")
        return self._services[name]

    def exists(self, name: str) -> bool:
        return name in self._services

    def remove(self, name: str) -> None:
        self._services.pop(name, None)

    def clear(self) -> None:
        self._services.clear()

    def list_services(self) -> list[str]:
        return sorted(self._services.keys())


container = ServiceContainer()