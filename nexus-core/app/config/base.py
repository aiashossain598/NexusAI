from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    app_name: str = "Nexus AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        extra="ignore"
    )