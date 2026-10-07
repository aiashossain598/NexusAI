from __future__ import annotations

import sys
from pathlib import Path

from app.agents.coding_agent import CodingAgent, ModelTurn
from app.core.policy import ConfirmationManager, WorkspacePolicy
from app.core.tool_executor import ToolExecutor
from app.events.event_bus import EventBus


class FakeModel:
    def __init__(self, turns: list[ModelTurn]) -> None:
        self.turns = turns
        self.responses: list[object] = []

    def generate(self, history, tools):
        return self.turns.pop(0)

    def function_responses(self, responses):
        self.responses.append(responses)
        return {"role": "user", "responses": responses}


def make_executor(tmp_path: Path, *, timeout: int = 1, limit: int = 50):
    events = EventBus()
    return ToolExecutor(WorkspacePolicy(tmp_path), ConfirmationManager(), events, timeout_seconds=timeout, max_output_chars=limit), events


def test_file_tools_and_traversal_are_policy_controlled(tmp_path: Path) -> None:
    executor, _ = make_executor(tmp_path)
    assert executor.write_file("new.txt", "hello").status == "ok"
    assert executor.read_file("new.txt").content == "hello"
    assert "new.txt" in executor.list_directory(".").content
    assert executor.read_file("../outside.txt").status == "blocked"
    assert executor.read_file(".env").status == "blocked"


def test_overwrite_and_destructive_commands_require_trusted_confirmation(tmp_path: Path) -> None:
    executor, _ = make_executor(tmp_path)
    target = tmp_path / "existing.txt"
    target.write_text("old", encoding="utf-8")
    pending = executor.write_file("existing.txt", "new")
    assert pending.status == "confirmation_required"
    assert not executor.confirmations.approve("not-a-real-id")
    assert executor.confirmations.approve(pending.confirmation_id or "")
    assert executor.write_file("existing.txt", "new", pending.confirmation_id).status == "ok"
    shell = executor.run_shell("rm temporary.txt")
    assert shell.status == "confirmation_required"


def test_shell_failure_timeout_and_output_limit(tmp_path: Path) -> None:
    executor, _ = make_executor(tmp_path, timeout=1, limit=10)
    (tmp_path / "fail.py").write_text("raise SystemExit(4)", encoding="utf-8")
    (tmp_path / "sleep.py").write_text("import time\ntime.sleep(2)", encoding="utf-8")
    (tmp_path / "output.py").write_text("print('x' * 100)", encoding="utf-8")
    failed = executor.run_shell(f'"{sys.executable}" fail.py')
    assert failed.status == "failed" and failed.exit_code == 4
    timed_out = executor.run_shell(f'"{sys.executable}" sleep.py')
    assert timed_out.status == "timeout"
    output = executor.run_shell(f'"{sys.executable}" output.py')
    assert output.truncated


def test_agent_executes_tools_through_executor_and_stops(tmp_path: Path) -> None:
    executor, events = make_executor(tmp_path)
    model = FakeModel([
        ModelTurn(tool_calls=(("write_file", {"path": "created.txt", "content": "ok"}),)),
        ModelTurn(text="Created it."),
    ])
    observed: list[str] = []
    events.subscribe("coding_tool.executed", lambda event: observed.append(event.payload["tool"]))
    output = list(CodingAgent(model, executor, events).run("Create a file"))
    assert (tmp_path / "created.txt").read_text() == "ok"
    assert observed == ["write_file"]
    assert output[-1] == {"type": "done"}


def test_agent_handles_unknown_tool_and_iteration_limit(tmp_path: Path) -> None:
    executor, events = make_executor(tmp_path)
    model = FakeModel([ModelTurn(tool_calls=(("not_a_tool", {}),)), ModelTurn()])
    output = list(CodingAgent(model, executor, events).run("Do work"))
    assert any(event["content"]["status"] == "blocked" for event in output if event["type"] == "tool_result")
    looping = FakeModel([ModelTurn(tool_calls=(("list_directory", {}),))] * 2)
    limited = list(CodingAgent(looping, executor, events, max_turns=1).run("Loop"))
    assert limited[-1]["type"] == "error"
