"""Tests for StepExecutor."""
import pytest

from engine.execution_step import ExecutionStep
from engine.step_executor import StepExecutor


class FakeLLMClient:
    """Fake LLM client that records calls and returns a fixed response."""

    def __init__(self, response: str = "fake response") -> None:
        self.response = response
        self.calls: list[dict] = []

    def chat(self, model: str, system: str, user: str) -> str:
        self.calls.append({"model": model, "system": system, "user": user})
        return self.response


def make_step() -> ExecutionStep:
    return ExecutionStep(
        module="code_review",
        system_prompt="You are a reviewer.",
        user_prompt="Review this code.",
    )


def test_step_executor_returns_new_step_with_result():
    client = FakeLLMClient("LLM output")
    executor = StepExecutor(client=client, model="test-model")
    step = make_step()
    result_step = executor.execute(step)
    assert result_step.result == "LLM output"


def test_step_executor_does_not_mutate_original_step():
    client = FakeLLMClient("output")
    executor = StepExecutor(client=client, model="test-model")
    step = make_step()
    executor.execute(step)
    assert step.result == ""


def test_step_executor_calls_llm_client_once():
    client = FakeLLMClient()
    executor = StepExecutor(client=client, model="test-model")
    executor.execute(make_step())
    assert len(client.calls) == 1


def test_step_executor_passes_correct_prompts_to_client():
    client = FakeLLMClient()
    executor = StepExecutor(client=client, model="mymodel")
    step = make_step()
    executor.execute(step)
    call = client.calls[0]
    assert call["model"] == "mymodel"
    assert call["system"] == step.system_prompt
    assert call["user"] == step.user_prompt
