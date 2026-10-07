"""Core policy and confirmation services for actions requested by agents."""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Decision(StrEnum):
    ALLOW = "allow"
    BLOCK = "block"
    CONFIRM = "confirm"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision: Decision
    reason: str
    path: Path | None = None


@dataclass(frozen=True, slots=True)
class ConfirmationRequest:
    id: str
    action: str
    summary: str


class ConfirmationManager:
    """Tracks approvals made by a UI or other trusted Core entry point.

    A model-supplied boolean is intentionally never an approval.
    """

    def __init__(self) -> None:
        self._requests: dict[str, ConfirmationRequest] = {}
        self._approved: set[str] = set()

    def request(self, action: str, summary: str) -> ConfirmationRequest:
        request = ConfirmationRequest(secrets.token_urlsafe(24), action, summary)
        self._requests[request.id] = request
        return request

    def approve(self, confirmation_id: str) -> bool:
        if confirmation_id not in self._requests:
            return False
        self._approved.add(confirmation_id)
        return True

    def consume_approval(self, confirmation_id: str | None, action: str) -> bool:
        if not confirmation_id or confirmation_id not in self._approved:
            return False
        request = self._requests.get(confirmation_id)
        if request is None or request.action != action:
            return False
        self._approved.remove(confirmation_id)
        self._requests.pop(confirmation_id, None)
        return True


class WorkspacePolicy:
    """Restricts coding tools to a single project workspace."""

    _PROTECTED_NAMES = frozenset({".env", ".env.production", ".env.development", ".env.testing", ".git"})
    _DESTRUCTIVE = re.compile(
        r"(?:^|[;&|]\s*)(?:rm|del|erase|rmdir|rd|remove-item|format|shutdown|restart-computer)\b",
        re.IGNORECASE,
    )
    _SHELL_CONTROL = re.compile(r"(?:&&|\|\||[;&|]|`|\$\(|>|<)")

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

    def resolve_path(self, requested_path: str) -> PolicyDecision:
        if not requested_path or not isinstance(requested_path, str):
            return PolicyDecision(Decision.BLOCK, "A non-empty path is required.")
        candidate = Path(requested_path)
        resolved = (candidate if candidate.is_absolute() else self.workspace / candidate).resolve()
        try:
            resolved.relative_to(self.workspace)
        except ValueError:
            return PolicyDecision(Decision.BLOCK, "Path escapes the configured workspace.")
        if any(part.casefold() in self._PROTECTED_NAMES for part in resolved.parts):
            return PolicyDecision(Decision.BLOCK, "Protected configuration and Git paths are unavailable to agents.")
        return PolicyDecision(Decision.ALLOW, "Path is inside the workspace.", resolved)

    def assess_shell(self, command: str, working_directory: Path) -> PolicyDecision:
        if not command or not isinstance(command, str):
            return PolicyDecision(Decision.BLOCK, "A non-empty command is required.")
        if not working_directory.is_dir():
            return PolicyDecision(Decision.BLOCK, "The working directory does not exist.")
        if self._DESTRUCTIVE.search(command):
            return PolicyDecision(Decision.CONFIRM, "Destructive command requires user confirmation.")
        if self._SHELL_CONTROL.search(command):
            return PolicyDecision(Decision.CONFIRM, "Shell control operators require user confirmation.")
        return PolicyDecision(Decision.ALLOW, "Command is permitted.")
