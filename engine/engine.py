"""Engine — orchestrates the single-pass execution pipeline.

Pipeline:
    Task → select_module → build_step → execute → refactor → result
"""
import json
import os
from pathlib import Path
from typing import Any

from companion.config.loader import load_config_file
from companion.prompting.builder import PromptBuilder
from companion.utils.logger import get_logger

from engine.execution_step import ExecutionStep
from engine.step_executor import OllamaClient, StepExecutor
from engine.task_controller import TaskController

logger = get_logger(__name__)

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")


def _load_json_template(path: str | Path) -> dict[str, Any]:
    """Load a JSON template from an explicit file path.

    This is a lightweight helper used by the legacy engine so that creating an
    Engine instance never triggers the companion ``get_config()`` / config
    validation path.  It intentionally has no dependency on
    ``companion.config`` beyond plain JSON file I/O.
    """
    resolved = Path(path) if Path(path).is_absolute() else Path(os.path.dirname(__file__)) / path
    if not resolved.exists():
        raise FileNotFoundError(f"Template not found: {resolved}")
    with resolved.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid template format (expected a JSON object): {resolved}")
    return payload


class Engine:
    """Single-pass execution engine.

    Constraints:
    * No loops
    * No recursion
    * No multi-step orchestration
    * LLM is only called inside StepExecutor
    """

    def __init__(self, config_path: str = _CONFIG_PATH) -> None:
        cfg = load_config_file(config_path)
        self._cfg = cfg

        engine_cfg = cfg["engine"]
        self._model: str = engine_cfg["model"]

        tc_cfg = cfg["task_controller"]
        self._controller = TaskController(
            mappings=tc_cfg["mappings"],
            default_module=tc_cfg["default_module"],
        )

        client = OllamaClient(
            base_url=engine_cfg["base_url"],
            model=self._model,
            timeout=engine_cfg["timeout"],
        )
        self._executor = StepExecutor(client=client, model=self._model)
        self._modules_cfg = cfg["modules"]
        self._prompt_builder = PromptBuilder()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self, task_type: str, context: dict[str, Any]) -> str:
        """Execute a single task and return the result string.

        Phases (in order, no branching):
        1. select_module
        2. build_step
        3. execute
        4. refactor
        """
        module_name = self._select_module(task_type)
        step = self._build_step(module_name, context)
        executed_step = self._execute(step)
        result = self._refactor(executed_step)
        return result

    # ------------------------------------------------------------------
    # Private phase methods
    # ------------------------------------------------------------------

    def _select_module(self, task_type: str) -> str:
        """Phase 1 of 4 — choose the module for this task."""
        module_name = self._controller.select_module(task_type)
        logger.info("[select_module] resolved module: %s", module_name)
        return module_name

    def _build_step(self, module_name: str, context: dict[str, Any]) -> ExecutionStep:
        """Phase 2 of 4 — build the ExecutionStep from template + context."""
        logger.info("[build_step] module=%s", module_name)
        template = self._load_module_template(module_name)
        user_prompt = self._build_user_prompt(template["user"], context)
        step = ExecutionStep(
            module=module_name,
            system_prompt=template["system"],
            user_prompt=user_prompt,
            context=context,
        )
        logger.info("[build_step] step created for module=%s", module_name)
        return step

    def _execute(self, step: ExecutionStep) -> ExecutionStep:
        """Phase 3 of 4 — delegate to StepExecutor (the only LLM caller)."""
        logger.info("[execute] dispatching step to StepExecutor, module=%s", step.module)
        executed = self._executor.execute(step)
        logger.info("[execute] step completed, module=%s", step.module)
        return executed

    def _refactor(self, step: ExecutionStep) -> str:
        """Phase 4 of 4 — non-mutating post-processing stub.

        In Phase 1 this method intentionally returns the result unchanged.
        It exists as an explicit phase boundary so that Phase 2 can attach
        real refactor logic here without touching the rest of the pipeline.
        """
        logger.info("[refactor] phase entered, module=%s (pass-through)", step.module)
        result = step.result
        logger.info("[refactor] phase complete, module=%s", step.module)
        return result

    def _load_module_template(self, module_name: str) -> dict[str, Any]:
        """Load the configured template payload for a module."""
        module_cfg = self._modules_cfg[module_name]
        template_path = os.path.join(
            os.path.dirname(__file__), "..", module_cfg["template"]
        )
        template = _load_json_template(template_path)
        missing_keys = [key for key in ("system", "user") if key not in template]
        if missing_keys:
            missing_keys_str = ", ".join(sorted(missing_keys))
            raise ValueError(
                f"Invalid template for module '{module_name}' at '{template_path}': "
                f"missing required key(s): {missing_keys_str}"
            )
        return template

    def _build_user_prompt(self, user_template: str, context: dict[str, Any]) -> str:
        """Build user prompt text from template and context."""
        return self._prompt_builder.build(
            {"system": "", "rules": [], "template": user_template},
            context,
        )
