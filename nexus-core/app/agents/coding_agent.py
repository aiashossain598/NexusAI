"""Nexus Coding Agent integration point."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Protocol

from app.core.tool_executor import ToolExecutor
from app.events.event import Event
from app.events.event_bus import EventBus


@dataclass(slots=True)
class ModelTurn:
    text: str = ""
    tool_calls: tuple[tuple[str, dict[str, Any]], ...] = ()
    provider_content: Any = None


class ModelClient(Protocol):
    def generate(self, history: list[Any], tools: tuple[dict[str, Any], ...]) -> ModelTurn: ...
    def function_responses(self, responses: list[tuple[str, dict[str, Any]]]) -> Any: ...


TOOL_DECLARATIONS: tuple[dict[str, Any], ...] = (
    {"name": "read_file", "parameters": {"path": "string"}},
    {"name": "write_file", "parameters": {"path": "string", "content": "string", "confirmation_id": "string?"}},
    {"name": "list_directory", "parameters": {"path": "string?"}},
    {"name": "run_shell", "parameters": {"command": "string", "working_dir": "string?", "confirmation_id": "string?"}},
)


class CodingAgent:
    def __init__(self, model: ModelClient, executor: ToolExecutor, events: EventBus, *, max_turns: int = 15) -> None:
        self.model, self.executor, self.events, self.max_turns = model, executor, events, max_turns

    def run(self, instruction: str) -> Iterator[dict[str, Any]]:
        if not instruction.strip():
            yield {"type": "error", "content": "A coding instruction is required."}
            return
        self.events.publish(Event("coding_agent.started", {"instruction_length": len(instruction)}))
        history: list[Any] = [{"role": "user", "text": instruction}]
        try:
            for _ in range(self.max_turns):
                turn = self.model.generate(history, TOOL_DECLARATIONS)
                if turn.text:
                    yield {"type": "text", "content": turn.text}
                history.append(turn.provider_content if turn.provider_content is not None else {"role": "model", "text": turn.text})
                if not turn.tool_calls:
                    self.events.publish(Event("coding_agent.completed"))
                    yield {"type": "done"}
                    return
                responses: list[tuple[str, dict[str, Any]]] = []
                for name, arguments in turn.tool_calls:
                    arguments = arguments if isinstance(arguments, dict) else {}
                    yield {"type": "tool_call", "name": name, "args": arguments}
                    payload = self.executor.execute(name, arguments).as_dict()
                    yield {"type": "tool_result", "name": name, "content": payload}
                    responses.append((name, payload))
                history.append(self.model.function_responses(responses))
            self.events.publish(Event("coding_agent.failed", {"reason": "maximum_tool_iterations"}))
            yield {"type": "error", "content": "Maximum tool iterations reached."}
        except Exception as exc:
            self.events.publish(Event("coding_agent.failed", {"reason": type(exc).__name__}))
            yield {"type": "error", "content": f"Coding agent failed safely: {exc}"}
