"""Tests for ExecutionStep."""
import pytest

from engine.execution_step import ExecutionStep


def test_execution_step_creation():
    step = ExecutionStep(
        module="code_review",
        system_prompt="You are a reviewer.",
        user_prompt="Review this code.",
        context={"code": "print('hello')"},
    )
    assert step.module == "code_review"
    assert step.system_prompt == "You are a reviewer."
    assert step.user_prompt == "Review this code."
    assert step.context == {"code": "print('hello')"}
    assert step.result == ""


def test_with_result_does_not_mutate_original():
    step = ExecutionStep(
        module="code_review",
        system_prompt="sys",
        user_prompt="usr",
    )
    updated = step.with_result("some output")
    assert step.result == ""
    assert updated.result == "some output"


def test_with_result_preserves_fields():
    step = ExecutionStep(
        module="code_review",
        system_prompt="sys",
        user_prompt="usr",
        context={"key": "value"},
    )
    updated = step.with_result("output")
    assert updated.module == step.module
    assert updated.system_prompt == step.system_prompt
    assert updated.user_prompt == step.user_prompt
    assert updated.context == step.context
