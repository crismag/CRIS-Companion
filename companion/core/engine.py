"""Core engine for step-based single-pass CRIS Companion execution."""

from __future__ import annotations

from pathlib import Path

from companion.controllers.task_controller import TaskController
from companion.core.executor import StepExecutor
from companion.integration.provider_factory import get_provider
from companion.utils.logger import get_logger


def _write_file(file_path: str, content: str) -> None:
    """Write content to disk, creating parent directories when needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _result_messages(settings: dict) -> dict:
    """Load result message text from settings."""
    messages = settings.get("messages", {})
    return {
        "generated": messages.get("generated", "Generated response"),
        "generated_and_saved": messages.get(
            "generated_and_saved",
            "Generated response and saved file",
        ),
    }


class Engine:
    """Single-pass engine using explicit execution steps."""

    def __init__(self, settings: dict, output_path: str | None = None) -> None:
        self.settings = settings
        self.output_path = output_path
        self.logger = get_logger("companion.engine")
        self.controller = TaskController()
        self.executor = StepExecutor(get_provider(settings))

    def _log_phase(self, phase_name: str) -> None:
        """Log phase transitions in a structured control-plane-friendly format."""
        self.logger.info("event=engine_phase phase=%s status=start", phase_name)

    def run(self, task: str) -> dict:
        """Execute one run via task->step->result single-pass workflow."""
        messages = _result_messages(self.settings)

        self._log_phase("Build execution step")
        step = self.controller.build_step(task)

        self._log_phase("Execute step")
        response = self.executor.execute(step)

        if self.output_path:
            _write_file(self.output_path, response + "\n")
            return {
                "status": "ok",
                "message": messages["generated_and_saved"],
                "response": response,
                "file_path": self.output_path,
            }

        return {
            "status": "ok",
            "message": messages["generated"],
            "response": response,
        }


def run_engine(task: str, settings: dict, output_path: str | None = None) -> dict:
    """Run a single engine execution."""
    return Engine(settings=settings, output_path=output_path).run(task)
