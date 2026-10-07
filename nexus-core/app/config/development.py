from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    environment: str = "development"
    debug: bool = True