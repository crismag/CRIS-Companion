"""Execution step model for single-pass task execution."""

from __future__ import annotations


class ExecutionStep:
    """LangGraph-compatible unit of execution for a single task step."""

    def __init__(self, name: str, intent: str, template: str, inputs: dict[str, str]) -> None:
        self.name = name
        self.intent = intent
        self.template = template
        self.inputs = inputs
