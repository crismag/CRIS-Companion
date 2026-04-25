"""StepExecutor — the single point of contact between the engine and the LLM.

No other module in the engine may call the LLM directly.
"""
import logging
from typing import Protocol

from engine.execution_step import ExecutionStep

logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    """Minimal protocol that any LLM backend must satisfy."""

    def chat(self, model: str, system: str, user: str) -> str:
        """Send a chat request and return the assistant response as a string."""
        ...


class OllamaClient:
    """Production LLM client backed by a local Ollama instance."""

    def __init__(self, base_url: str, model: str, timeout: int = 120) -> None:
        self._base_url = base_url
        self._model = model
        self._timeout = timeout

    def chat(self, model: str, system: str, user: str) -> str:
        import json
        import urllib.request

        payload = json.dumps(
            {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
            }
        ).encode()

        url = f"{self._base_url}/api/chat"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            data = json.loads(resp.read().decode())
        return data["message"]["content"]


class StepExecutor:
    """Executes an :class:`~engine.execution_step.ExecutionStep` via the LLM.

    This is the **only** class allowed to call the LLM.  All engine phases
    must go through this executor.
    """

    def __init__(self, client: LLMClient, model: str) -> None:
        self._client = client
        self._model = model

    def execute(self, step: ExecutionStep) -> ExecutionStep:
        """Execute *step* and return a new step with the result populated.

        The original *step* is not modified.
        """
        logger.info("[execute] module=%s — calling LLM", step.module)
        response = self._client.chat(
            model=self._model,
            system=step.system_prompt,
            user=step.user_prompt,
        )
        logger.info("[execute] module=%s — response received", step.module)
        return step.with_result(response)
