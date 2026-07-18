from .base import BaseConfig


class ProductionConfig(BaseConfig):
    environment: str = "production"
    debug: bool = False