"""Coding template loading for CRIS Companion."""

from __future__ import annotations

from pathlib import Path

from companion.config.template_loader import TemplateLoader


def load_coding_template(base_path: Path | None = None) -> dict:
    """Load coding template data from the active template profile.

    Returns a template dictionary with keys:
    - system: system prompt text
    - rules: list of rule strings
    - template: format string
    """
    return TemplateLoader(base_path=base_path).load("coding")
