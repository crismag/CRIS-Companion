"""Coding template loading for CRIS Companion."""

from __future__ import annotations

DEFAULT_CODING_SYSTEM_PROMPT = (
    "You are CRIS Companion. Generate clean Python code only, no markdown fencing."
)
DEFAULT_CODING_TEMPLATE = "{system}\nTask: {task}"


def load_coding_template(settings: dict | None = None) -> dict:
    """Load coding template data from runtime settings.

    Returns a template dictionary with keys:
    - system: system prompt text
    - template: format string
    """
    runtime_settings = settings or {}
    templates = runtime_settings.get("templates", {})
    coding_template = templates.get("coding", {})

    return {
        "system": coding_template.get("system", DEFAULT_CODING_SYSTEM_PROMPT),
        "template": coding_template.get("template", DEFAULT_CODING_TEMPLATE),
    }
