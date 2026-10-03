"""Local/Offline fallback model client when external LLM API keys are not provided."""

from __future__ import annotations

import re
from typing import Any

from app.agents.coding_agent import ModelTurn


class LocalFallbackModelClient:
    """Provides a safe, local fallback model client for testing and offline execution."""

    def __init__(self) -> None:
        self._turn_count = 0

    def generate(self, history: list[Any], tools: tuple[dict[str, Any], ...]) -> ModelTurn:
        self._turn_count += 1
        last_turn = history[-1] if history else {}

        # If previous turn was a function response, summarize the tool results
        if isinstance(last_turn, dict) and last_turn.get("role") == "user" and "responses" in last_turn:
            responses = last_turn.get("responses", [])
            summary_parts = []
            for name, payload in responses:
                status = payload.get("status", "unknown") if isinstance(payload, dict) else "done"
                summary_parts.append(f"Tool `{name}` completed with status: {status}.")
            return ModelTurn(text=" ".join(summary_parts) + " Task completed.")

        user_text = ""
        for item in reversed(history):
            if isinstance(item, dict) and item.get("role") == "user" and "text" in item:
                user_text = item["text"]
                break

        user_lower = user_text.lower()

        # Check if user instruction asks to list files/directory
        if "list" in user_lower and ("file" in user_lower or "dir" in user_lower or "folder" in user_lower):
            return ModelTurn(tool_calls=(("list_directory", {"path": "."}),))

        # Check if user instruction asks to read a file
        read_match = re.search(r"read (?:file )?['\"]?([a-zA-Z0-9_\-\.\/\\]+)['\"]?", user_lower)
        if read_match:
            filename = read_match.group(1)
            return ModelTurn(tool_calls=(("read_file", {"path": filename}),))

        return ModelTurn(
            text=(
                f"Nexus AI received your prompt: \"{user_text}\". "
                "Backend is running in local fallback mode. "
                "Provide GEMINI_API_KEY in .env to enable full Gemini reasoning capabilities."
            )
        )

    def function_responses(self, responses: list[tuple[str, dict[str, Any]]]) -> Any:
        return {"role": "user", "responses": responses}
