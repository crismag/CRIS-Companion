"""End-to-end tests for the Engine using a fake LLM client."""
import os
import sys
import types
import pytest

# Ensure repo root is on sys.path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.execution_step import ExecutionStep
from engine.step_executor import StepExecutor
from engine.task_controller import TaskController
from engine.engine import Engine


class FakeLLMClient:
    def __init__(self, response: str = "engine test output") -> None:
        self.response = response
        self.call_count = 0

    def chat(self, model: str, system: str, user: str) -> str:
        self.call_count += 1
        return self.response


def make_engine_with_fake_client(tmp_path, response="test result") -> tuple[Engine, FakeLLMClient]:
    """Build a real Engine wired to a fake LLM client."""
    import yaml, json, pathlib

    # Write a minimal config.yaml
    cfg = {
        "engine": {"model": "test-model", "base_url": "http://localhost:11434", "timeout": 10},
        "modules": {
            "code_review": {"template": "templates/code_review.json", "description": "Review"},
            "code_generation": {"template": "templates/code_generation.json", "description": "Gen"},
            "refactor": {"template": "templates/refactor.json", "description": "Refactor"},
        },
        "task_controller": {
            "default_module": "code_review",
            "mappings": {"review": "code_review", "generate": "code_generation", "refactor": "refactor"},
        },
        "logging": {"level": "DEBUG"},
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.dump(cfg))

    # Copy templates into tmp_path
    repo_root = pathlib.Path(__file__).parent.parent
    tmpl_dir = tmp_path / "templates"
    tmpl_dir.mkdir()
    for name in ("code_review.json", "code_generation.json", "refactor.json"):
        src = repo_root / "templates" / name
        (tmpl_dir / name).write_text(src.read_text())

    engine = Engine(config_path=str(config_path))

    # Inject fake client
    fake = FakeLLMClient(response=response)
    executor = StepExecutor(client=fake, model="test-model")
    engine._executor = executor

    return engine, fake


def test_engine_run_returns_result(tmp_path):
    engine, fake = make_engine_with_fake_client(tmp_path, response="review output")
    result = engine.run(task_type="review", context={"code": "x = 1"})
    assert result == "review output"


def test_engine_calls_llm_exactly_once(tmp_path):
    engine, fake = make_engine_with_fake_client(tmp_path)
    engine.run(task_type="review", context={"code": "x = 1"})
    assert fake.call_count == 1


def test_engine_refactor_phase_does_not_modify_result(tmp_path):
    """The refactor phase must be a pass-through in Phase 1."""
    engine, fake = make_engine_with_fake_client(tmp_path, response="original result")
    result = engine.run(task_type="review", context={"code": "x = 1"})
    assert result == "original result"


def test_engine_select_module_uses_task_controller(tmp_path):
    engine, _ = make_engine_with_fake_client(tmp_path)
    # The controller has a static mapping; verify it resolves the module
    module = engine._controller.select_module("generate")
    assert module == "code_generation"


def test_engine_unknown_task_type_uses_default(tmp_path):
    engine, fake = make_engine_with_fake_client(tmp_path, response="default output")
    result = engine.run(task_type="unknown", context={"code": "x = 1"})
    assert result == "default output"
