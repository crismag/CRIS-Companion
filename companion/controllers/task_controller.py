"""Task controller that builds a single execution step."""

from __future__ import annotations

from companion.core.step import ExecutionStep


class TaskController:
    """Build the initial step from task input in single-pass mode."""

    def build_step(self, task: str) -> ExecutionStep:
        return ExecutionStep(
            name="generate_code",
            intent="coding",
            template="coding",
            inputs={"task": task.strip()},
        )
