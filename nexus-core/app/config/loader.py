import os

from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig


def load_config():
    env = os.getenv("NEXUS_ENV", "development").lower()

    if env == "production":
        return ProductionConfig()

    if env == "testing":
        return TestingConfig()

    return DevelopmentConfig()


settings = load_config()