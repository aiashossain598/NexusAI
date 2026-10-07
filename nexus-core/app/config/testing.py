from .base import BaseConfig


class TestingConfig(BaseConfig):
    environment: str = "testing"
    debug: bool = True