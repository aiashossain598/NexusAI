from pathlib import Path

from app.agents.coding_agent import CodingAgent
from app.agents.gemini import GeminiModelClient
from app.config.loader import settings
from app.core.container import container
from app.core.policy import ConfirmationManager, WorkspacePolicy
from app.core.registry import registry
from app.core.tool_executor import ToolExecutor
from app.events.event import Event
from app.events.event_bus import event_bus
from app.utils.logger import app_logger
from app.plugins.loader import plugin_loader

class Bootstrap:
    def start(self) -> None:
        workspace_policy = WorkspacePolicy(Path.cwd())
        confirmation_manager = ConfirmationManager()
        tool_executor = ToolExecutor(workspace_policy, confirmation_manager, event_bus)
        # Register core services
        container.register("settings", settings)
        container.register("logger", app_logger)
        container.register("event_bus", event_bus)
        container.register("plugin_loader", plugin_loader)
        container.register("workspace_policy", workspace_policy)
        container.register("confirmation_manager", confirmation_manager)
        container.register("tool_executor", tool_executor)

        registry.add("settings", settings)
        registry.add("logger", app_logger)
        registry.add("event_bus", event_bus)
        registry.add("plugin_loader", plugin_loader)
        registry.add("workspace_policy", workspace_policy)
        registry.add("confirmation_manager", confirmation_manager)
        registry.add("tool_executor", tool_executor)
        registry.add(
            "coding_agent_factory",
            lambda model=None: CodingAgent(model or GeminiModelClient(), tool_executor, event_bus),
        )

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
