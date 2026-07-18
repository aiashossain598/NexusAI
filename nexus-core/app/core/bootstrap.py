from app.config.loader import settings
from app.core.container import container
from app.utils.logger import app_logger
from app.events.event import Event
from app.events.event_bus import event_bus


class Bootstrap:

    def start(self) -> None:
        container.register("settings", settings)
        container.register("logger", app_logger)
        container.register("event_bus", event_bus)

        def startup_listener(event: Event):
            app_logger.info(f"Event Received -> {event.name}")

        event_bus.subscribe("startup", startup_listener)

        app_logger.info("=" * 60)
        app_logger.info(f"Starting {settings.app_name}")
        app_logger.info(f"Version : {settings.app_version}")
        app_logger.info(f"Environment : {settings.environment}")
        app_logger.info(f"Registered Services : {container.list_services()}")

        event_bus.publish(Event("startup"))

        app_logger.info("Bootstrap completed successfully.")
        app_logger.info("=" * 60)