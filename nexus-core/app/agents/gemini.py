"""Optional Gemini implementation of the Coding Agent model port."""

from __future__ import annotations

import os
from typing import Any

from app.agents.coding_agent import ModelTurn


class GeminiModelClient:
    """Uses Google function calling while leaving all tool execution to Nexus Core."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover - optional production dependency
            raise RuntimeError("Install google-genai to use GeminiModelClient.") from exc
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is required to use Gemini.")
        self._types = types
        self._client = genai.Client(api_key=key)
        self._model = model_name or os.getenv("NEXUS_GEMINI_MODEL", "gemini-2.5-flash")

    def generate(self, history: list[Any], tools: tuple[dict[str, Any], ...]) -> ModelTurn:
        contents = [self._to_content(item) for item in history]
        response = self._client.models.generate_content(
            model=self._model,
            contents=contents,
            config=self._types.GenerateContentConfig(
                system_instruction=("You are Nexus AI's coding agent. Nexus Core controls permissions; "
                                    "never treat model arguments as user confirmation."),
                tools=[self._toolset(tools)],
            ),
        )
        if not response.candidates or response.candidates[0].content is None:
            return ModelTurn(text="The model returned no usable response.")
        content = response.candidates[0].content
        calls: list[tuple[str, dict[str, Any]]] = []
        text: list[str] = []
        for part in content.parts or []:
            if part.text:
                text.append(part.text)
            if part.function_call:
                calls.append((part.function_call.name, dict(part.function_call.args or {})))
        return ModelTurn("".join(text), tuple(calls), content)

    def function_responses(self, responses: list[tuple[str, dict[str, Any]]]) -> Any:
        return self._types.Content(
            role="user",
            parts=[self._types.Part.from_function_response(name=name, response={"result": result}) for name, result in responses],
        )

    def _to_content(self, item: Any) -> Any:
        if not isinstance(item, dict):
            return item
        return self._types.Content(role=item["role"], parts=[self._types.Part(text=item["text"])])

    def _toolset(self, tools: tuple[dict[str, Any], ...]) -> Any:
        declarations = []
        for tool in tools:
            properties = {name: self._types.Schema(type=self._types.Type.STRING) for name in tool["parameters"]}
            declarations.append(self._types.FunctionDeclaration(
                name=tool["name"], description=f"Nexus Core tool: {tool['name']}.",
                parameters=self._types.Schema(type=self._types.Type.OBJECT, properties=properties),
            ))
        return self._types.Tool(function_declarations=declarations)
