"""Tests for TaskController."""
import pytest

from engine.task_controller import TaskController


MAPPINGS = {
    "review": "code_review",
    "generate": "code_generation",
    "refactor": "refactor",
}
DEFAULT = "code_review"


def make_controller() -> TaskController:
    return TaskController(mappings=MAPPINGS, default_module=DEFAULT)


def test_select_module_known_task():
    ctrl = make_controller()
    assert ctrl.select_module("review") == "code_review"
    assert ctrl.select_module("generate") == "code_generation"
    assert ctrl.select_module("refactor") == "refactor"


def test_select_module_unknown_task_falls_back_to_default():
    ctrl = make_controller()
    assert ctrl.select_module("unknown_task") == DEFAULT


def test_select_module_empty_string_falls_back_to_default():
    ctrl = make_controller()
    assert ctrl.select_module("") == DEFAULT
