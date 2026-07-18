from app.config.loader import settings
from app.core.container import container
from app.core.registry import registry
from app.events.event import Event
from app.events.event_bus import event_bus
from app.utils.logger import app_logger


class Bootstrap:
    def start(self) -> None:
        # Register core services
        container.register("settings", settings)
        container.register("logger", app_logger)
        container.register("event_bus", event_bus)

        registry.add("settings", settings)
        registry.add("logger", app_logger)
        registry.add("event_bus", event_bus)

        # Event listener
        def startup_listener(event: Event) -> None:
            app_logger.info(f"Event Received -> {event.name}")

        event_bus.subscribe("startup", startup_listener)

        # Startup logs
        app_logger.info("=" * 60)
        app_logger.info(f"Starting {settings.app_name}")
        app_logger.info(f"Version : {settings.app_version}")
        app_logger.info(f"Environment : {settings.environment}")
        app_logger.info(f"Registered Services : {container.list_services()}")
        app_logger.info(f"Registry : {list(registry.all().keys())}")

        # Publish startup event
        event_bus.publish(Event("startup"))

        app_logger.info("Bootstrap completed successfully.")
        app_logger.info("=" * 60)