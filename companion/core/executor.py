"""Step executor for running execution steps through a provider."""

from __future__ import annotations

from companion.config.template_loader import TemplateLoader
from companion.core.step import ExecutionStep
from companion.prompting.builder import PromptBuilder


class StepExecutor:
    """Execute a single step by resolving template and calling provider."""

    def __init__(self, provider, template_loader: TemplateLoader | None = None) -> None:
        self.provider = provider
        self.templates = template_loader or TemplateLoader()
        self._builder = PromptBuilder()

    def execute(self, step: ExecutionStep) -> str:
        """Render prompt for an execution step and call provider."""
        template_payload = self.templates.load(step.template)
        prompt = self._builder.build(template_payload, step.inputs)
        return self.provider.generate(prompt)
