"""Policy-enforced implementations of coding-agent tools."""

from __future__ import annotations

import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.policy import ConfirmationManager, Decision, WorkspacePolicy
from app.events.event import Event
from app.events.event_bus import EventBus
from app.utils.logger import app_logger


@dataclass(frozen=True, slots=True)
class ToolResult:
    status: str
    content: str
    exit_code: int | None = None
    confirmation_id: str | None = None
    truncated: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ToolExecutor:
    def __init__(
        self,
        policy: WorkspacePolicy,
        confirmations: ConfirmationManager,
        events: EventBus,
        *,
        timeout_seconds: int = 120,
        max_output_chars: int = 8_000,
    ) -> None:
        self.policy = policy
        self.confirmations = confirmations
        self.events = events
        self.timeout_seconds = timeout_seconds
        self.max_output_chars = max_output_chars

    def execute(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        self.events.publish(Event("coding_tool.requested", {"tool": name}))
        try:
            result = {
                "read_file": self.read_file,
                "write_file": self.write_file,
                "list_directory": self.list_directory,
                "run_shell": self.run_shell,
            }.get(name)
            if result is None:
                return self._blocked(name, "Unknown tool.")
            output = result(**arguments)
        except (TypeError, ValueError) as exc:
            output = ToolResult("error", f"Invalid arguments: {exc}")
        except OSError as exc:
            app_logger.exception("Coding tool failed: {}", name)
            output = ToolResult("error", f"Tool execution failed: {exc}")
        self.events.publish(Event("coding_tool.executed", {"tool": name, "status": output.status}))
        return output

    def read_file(self, path: str) -> ToolResult:
        resolved = self.policy.resolve_path(path)
        if resolved.decision is Decision.BLOCK:
            return self._blocked("read_file", resolved.reason)
        assert resolved.path is not None
        if not resolved.path.is_file():
            return ToolResult("error", "Path is not a readable file.")
        text = resolved.path.read_text(encoding="utf-8", errors="replace")
        return self._truncate("ok", text, "file.read", str(resolved.path.relative_to(self.policy.workspace)))

    def write_file(self, path: str, content: str, confirmation_id: str | None = None) -> ToolResult:
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        resolved = self.policy.resolve_path(path)
        if resolved.decision is Decision.BLOCK:
            return self._blocked("write_file", resolved.reason)
        assert resolved.path is not None
        action = f"write:{resolved.path}"
        if resolved.path.exists() and not self.confirmations.consume_approval(confirmation_id, action):
            return self._confirmation(action, f"Overwrite {resolved.path.relative_to(self.policy.workspace)}")
        resolved.path.parent.mkdir(parents=True, exist_ok=True)
        resolved.path.write_text(content, encoding="utf-8")
        self.events.publish(Event("file.write", {"path": str(resolved.path), "characters": len(content)}))
        return ToolResult("ok", f"Wrote {len(content)} characters to {resolved.path.relative_to(self.policy.workspace)}.")

    def list_directory(self, path: str = ".") -> ToolResult:
        resolved = self.policy.resolve_path(path)
        if resolved.decision is Decision.BLOCK:
            return self._blocked("list_directory", resolved.reason)
        assert resolved.path is not None
        if not resolved.path.is_dir():
            return ToolResult("error", "Path is not a directory.")
        listing = "\n".join(item.name for item in sorted(resolved.path.iterdir(), key=lambda item: item.name.casefold()))
        return self._truncate("ok", listing or "(empty directory)", "file.listed", str(resolved.path.relative_to(self.policy.workspace)))

    def run_shell(self, command: str, working_dir: str = ".", confirmation_id: str | None = None) -> ToolResult:
        location = self.policy.resolve_path(working_dir)
        if location.decision is Decision.BLOCK or location.path is None:
            return self._blocked("run_shell", location.reason)
        decision = self.policy.assess_shell(command, location.path)
        action = f"shell:{location.path}:{command}"
        if decision.decision is Decision.BLOCK:
            return self._blocked("run_shell", decision.reason)
        if decision.decision is Decision.CONFIRM and not self.confirmations.consume_approval(confirmation_id, action):
            return self._confirmation(action, command)
        self.events.publish(Event("shell.command.requested", {"command": command, "working_dir": str(location.path)}))
        try:
            completed = subprocess.run(
                command, shell=True, cwd=location.path, capture_output=True, text=True,
                timeout=self.timeout_seconds, env=self._safe_environment(),
            )
        except subprocess.TimeoutExpired:
            return ToolResult("timeout", f"Command timed out after {self.timeout_seconds} seconds.")
        content = f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        result = self._truncate("ok" if completed.returncode == 0 else "failed", content)
        result = ToolResult(result.status, result.content, completed.returncode, truncated=result.truncated)
        self.events.publish(Event("shell.command.executed", {"exit_code": completed.returncode, "status": result.status}))
        return result

    def _safe_environment(self) -> dict[str, str]:
        return {key: value for key, value in os.environ.items() if key.upper() not in {"GEMINI_API_KEY", "OPENAI_API_KEY"}}

    def _truncate(self, status: str, content: str, event_name: str | None = None, path: str | None = None) -> ToolResult:
        truncated = len(content) > self.max_output_chars
        if event_name:
            self.events.publish(Event(event_name, {"path": path}))
        return ToolResult(status, content[: self.max_output_chars], truncated=truncated)

    def _blocked(self, tool: str, reason: str) -> ToolResult:
        self.events.publish(Event("coding_tool.blocked", {"tool": tool, "reason": reason}))
        return ToolResult("blocked", reason)

    def _confirmation(self, action: str, summary: str) -> ToolResult:
        request = self.confirmations.request(action, summary)
        self.events.publish(Event("coding_tool.confirmation_required", {"action": action, "confirmation_id": request.id}))
        return ToolResult("confirmation_required", "User confirmation is required before this action can run.", confirmation_id=request.id)
