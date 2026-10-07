from collections import defaultdict
from typing import Callable

from app.events.event import Event


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[Event], None]) -> None:
        self._listeners[event_name].append(callback)

    def publish(self, event: Event) -> None:
        for callback in self._listeners[event.name]:
            callback(event)


event_bus = EventBus()