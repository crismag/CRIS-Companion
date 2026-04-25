"""UI adapter — thin bridge between the UI layer and the engine.

Rules:
* No business logic here.
* All execution goes through :class:`engine.engine.Engine`.
* The adapter surfaces logs, phases, and the final result.
"""
from typing import Any

from companion.utils.logger import get_logger
from engine.engine import Engine

logger = get_logger(__name__)


class EngineAdapter:
    """Adapter that the UI layer uses to invoke the engine.

    The UI must not instantiate the Engine directly or call any engine
    internals.  All interaction goes through this adapter.
    """

    def __init__(self, engine: Engine | None = None) -> None:
        self._engine = engine or Engine()

    def run_task(self, task_type: str, context: dict[str, Any]) -> dict[str, Any]:
        """Run a task and return a structured response for the UI.

        Returns a dict with keys:
        * ``status``: ``"ok"`` or ``"error"``
        * ``result``: the engine output string (empty on error)
        * ``error``: error message (empty on success)
        """
        logger.info("[adapter] run_task called, task_type=%r", task_type)
        try:
            result = self._engine.run(task_type=task_type, context=context)
            logger.info("[adapter] run_task succeeded, task_type=%r", task_type)
            return {"status": "ok", "result": result, "error": ""}
        except Exception as exc:  # noqa: BLE001
            logger.error("[adapter] run_task failed, task_type=%r: %s", task_type, exc)
            return {"status": "error", "result": "", "error": str(exc)}
