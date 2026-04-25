"""TaskController — static mapping from task type to module name."""
import logging

logger = logging.getLogger(__name__)

# Type alias
TaskType = str
ModuleName = str


class TaskController:
    """Maps task types to module names using a static configuration table.

    No dynamic dispatch, no recursion, no loops over task lists.
    """

    def __init__(self, mappings: dict[TaskType, ModuleName], default_module: ModuleName) -> None:
        self._mappings = mappings
        self._default_module = default_module

    def select_module(self, task_type: TaskType) -> ModuleName:
        """Return the module name for *task_type*.

        Falls back to the configured default module when the task type is
        not found in the static mapping table.
        """
        module = self._mappings.get(task_type, self._default_module)
        logger.info("[select_module] task_type=%r → module=%r", task_type, module)
        return module
