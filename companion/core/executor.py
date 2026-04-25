"""Step executor for running execution steps through a provider."""

from __future__ import annotations

from companion.config.template_loader import TemplateLoader
from companion.core.step import ExecutionStep


class StepExecutor:
    """Execute a single step by resolving template and calling provider."""

    def __init__(self, provider, template_loader: TemplateLoader | None = None) -> None:
        self.provider = provider
        self.templates = template_loader or TemplateLoader()

    def execute(self, step: ExecutionStep) -> str:
        """Render prompt for an execution step and call provider."""
        template_payload = self.templates.load(step.template)
        rules_text = "\n".join(template_payload["rules"])
        prompt = template_payload["template"].format(
            system=template_payload["system"],
            rules=rules_text,
            **step.inputs,
        )
        return self.provider.generate(prompt)
