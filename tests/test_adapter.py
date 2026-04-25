"""Tests for the UI EngineAdapter."""
import pytest

from engine.execution_step import ExecutionStep
from engine.step_executor import StepExecutor
from engine.engine import Engine
from ui.adapter import EngineAdapter


class FakeEngine:
    """Fake engine that returns a fixed result or raises an exception."""

    def __init__(self, result: str = "adapter result", raise_exc: Exception | None = None) -> None:
        self._result = result
        self._raise = raise_exc
        self.calls: list[dict] = []

    def run(self, task_type: str, context: dict) -> str:
        self.calls.append({"task_type": task_type, "context": context})
        if self._raise:
            raise self._raise
        return self._result


def test_adapter_run_task_ok():
    fake = FakeEngine(result="some output")
    adapter = EngineAdapter(engine=fake)
    response = adapter.run_task(task_type="review", context={"code": "x = 1"})
    assert response["status"] == "ok"
    assert response["result"] == "some output"
    assert response["error"] == ""


def test_adapter_run_task_error():
    fake = FakeEngine(raise_exc=RuntimeError("LLM unreachable"))
    adapter = EngineAdapter(engine=fake)
    response = adapter.run_task(task_type="review", context={"code": "x = 1"})
    assert response["status"] == "error"
    assert response["result"] == ""
    assert "LLM unreachable" in response["error"]


def test_adapter_delegates_to_engine():
    fake = FakeEngine()
    adapter = EngineAdapter(engine=fake)
    adapter.run_task(task_type="generate", context={"description": "test", "language": "python"})
    assert len(fake.calls) == 1
    assert fake.calls[0]["task_type"] == "generate"
