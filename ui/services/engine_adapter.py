"""Engine adapter service for Streamlit UI integration."""

from __future__ import annotations

import logging
from typing import Callable

from companion.core.engine import Engine


class SessionLogHandler(logging.Handler):
    """Logging handler that forwards engine logs to UI callback."""

    def __init__(self, on_log: Callable[[str], None]):
        super().__init__()
        self.on_log = on_log

    def emit(self, record: logging.LogRecord) -> None:
        self.on_log(self.format(record))


def _attach_ui_handler(
    engine_logger: logging.Logger,
    on_log: Callable[[str], None],
) -> SessionLogHandler:
    """Attach UI log handler after removing stale handlers from reruns."""
    for handler in list(engine_logger.handlers):
        if isinstance(handler, SessionLogHandler):
            engine_logger.removeHandler(handler)

    ui_handler = SessionLogHandler(on_log)
    ui_handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    engine_logger.addHandler(ui_handler)
    return ui_handler


def execute_task(
    task: str,
    settings: dict,
    output_path: str | None,
    model_override: str | None,
    on_log: Callable[[str], None],
) -> dict:
    """Execute a task through Engine while streaming logs back to UI."""
    runtime_settings = dict(settings)

    if model_override:
        runtime_settings["primary_model"] = model_override

    engine = Engine(settings=runtime_settings, output_path=output_path)
    ui_handler = _attach_ui_handler(engine.logger, on_log)

    try:
        return engine.run(task)
    finally:
        if ui_handler in engine.logger.handlers:
            engine.logger.removeHandler(ui_handler)
