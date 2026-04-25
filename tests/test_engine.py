"""Tests for CRIS Companion step-based engine behavior."""

from __future__ import annotations

from pathlib import Path

import companion.core.engine as engine_module
from companion.controllers.task_controller import TaskController
from companion.core.executor import StepExecutor
from companion.core.engine import run_engine
from companion.core.step import ExecutionStep


class _FakeProvider:
    """Simple provider stub for deterministic unit tests."""

    def __init__(self, response: str = "print('ok')") -> None:
        self.response = response
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


class _FakeTemplateLoader:
    """Template loader stub that returns a coding template."""

    def load(self, name: str) -> dict:
        assert name == "coding"
        return {
            "system": "You are CRIS Companion",
            "rules": ["Return code only"],
            "template": "{system}\n\nRules:\n{rules}\n\nTask:\n{task}\n\nOutput:",
        }


def _settings() -> dict:
    """Return minimal settings for engine tests."""
    return {
        "ollama_url": "http://localhost:11434",
        "primary_model": "x",
        "fallback_model": "y",
        "request_timeout_seconds": 1,
    }


def test_task_controller_builds_single_coding_step() -> None:
    """TaskController should always map task input to one coding step."""
    step = TaskController().build_step("  create a hello world script  ")

    assert step.name == "generate_code"
    assert step.intent == "coding"
    assert step.template == "coding"
    assert step.inputs == {"task": "create a hello world script"}


def test_step_executor_renders_prompt_and_calls_provider() -> None:
    """StepExecutor should build prompt from template and dispatch to provider."""
    provider = _FakeProvider(response="print('hello')")
    executor = StepExecutor(provider, template_loader=_FakeTemplateLoader())
    step = ExecutionStep(
        name="generate_code",
        intent="coding",
        template="coding",
        inputs={"task": "create a hello world script"},
    )

    result = executor.execute(step)

    assert result == "print('hello')"
    assert provider.prompts
    assert "You are CRIS Companion" in provider.prompts[0]
    assert "Task:\ncreate a hello world script" in provider.prompts[0]


def test_engine_returns_generated_response(monkeypatch) -> None:
    """Engine should return provider output for a plain task."""
    monkeypatch.setattr(engine_module, "get_provider", lambda settings: _FakeProvider("print(1)"))

    result = run_engine("write a python function to add two numbers", _settings())

    assert result["status"] == "ok"
    assert result["response"] == "print(1)"


def test_engine_writes_file_when_output_path_is_provided(tmp_path: Path, monkeypatch) -> None:
    """Engine should write output when output_path is explicitly set."""
    monkeypatch.setattr(engine_module, "get_provider", lambda settings: _FakeProvider("print('file')"))
    target_file = tmp_path / "hello.py"

    result = run_engine(
        "create hello world script",
        _settings(),
        output_path=str(target_file),
    )

    assert result["status"] == "ok"
    assert result["file_path"] == str(target_file)
    assert target_file.exists()
    assert target_file.read_text(encoding="utf-8").strip() == "print('file')"
