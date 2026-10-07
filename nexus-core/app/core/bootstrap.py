from pathlib import Path

from app.agents.coding_agent import CodingAgent
from app.agents.gemini import GeminiModelClient
from app.agents.local_client import LocalFallbackModelClient
from app.config.loader import settings
from app.core.container import container
from app.core.policy import ConfirmationManager, WorkspacePolicy
from app.core.registry import registry
from app.core.tool_executor import ToolExecutor
from app.events.event import Event
from app.events.event_bus import event_bus
from app.memory.manager import memory_manager
from app.plugins.loader import plugin_loader
from app.utils.logger import app_logger


class Bootstrap:
    _initialized: bool = False

    def start(self) -> None:
        if Bootstrap._initialized:
            return
        Bootstrap._initialized = True

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
        container.register("memory_manager", memory_manager)

        registry.add("settings", settings)
        registry.add("logger", app_logger)
        registry.add("event_bus", event_bus)
        registry.add("plugin_loader", plugin_loader)
        registry.add("workspace_policy", workspace_policy)
        registry.add("confirmation_manager", confirmation_manager)
        registry.add("tool_executor", tool_executor)
        registry.add("memory_manager", memory_manager)

        def make_agent(model=None):
            if model is None:
                try:
                    model = GeminiModelClient()
                except Exception:
                    model = LocalFallbackModelClient()
            return CodingAgent(model, tool_executor, event_bus)

        registry.add("coding_agent_factory", make_agent)

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
