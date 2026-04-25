"""Prompt builder isolated from engine and executor."""

from __future__ import annotations


class PromptBuilder:
    """Build text prompts from template payloads and execution inputs."""

    def build(self, template_payload: dict, inputs: dict[str, str]) -> str:
        rules = template_payload.get("rules", [])
        rules_text = "\n".join(str(rule) for rule in rules)
        template_text = str(template_payload.get("template", ""))

        return template_text.format(
            system=template_payload.get("system", ""),
            rules=rules_text,
            **inputs,
        )
