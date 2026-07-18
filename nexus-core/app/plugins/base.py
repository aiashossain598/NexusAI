from abc import ABC, abstractmethod


class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...