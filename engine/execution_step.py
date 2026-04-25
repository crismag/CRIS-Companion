"""ExecutionStep — immutable value object representing a single engine step."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionStep:
    """Represents one execution unit passed through the engine.

    All fields are set at construction time.  ``result`` is populated by
    :class:`engine.step_executor.StepExecutor` after the LLM call returns.
    The object itself is never mutated after that assignment; callers should
    treat it as effectively immutable once ``result`` is set.
    """

    module: str
    system_prompt: str
    user_prompt: str
    context: dict[str, Any] = field(default_factory=dict)
    result: str = ""

    def with_result(self, result: str) -> "ExecutionStep":
        """Return a new ExecutionStep that is identical except for ``result``.

        This keeps the original step unchanged, satisfying the non-mutating
        contract required by the refactor phase.
        """
        return ExecutionStep(
            module=self.module,
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt,
            context=dict(self.context),
            result=result,
        )
