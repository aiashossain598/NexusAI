from app.config.settings import settings
from app.utils.logger import app_logger


class Bootstrap:

    def start(self) -> None:
        app_logger.info("=" * 60)
        app_logger.info(f"Starting {settings.app_name}")
        app_logger.info(f"Version : {settings.version}")
        app_logger.info("Bootstrap completed successfully.")
        app_logger.info("=" * 60)