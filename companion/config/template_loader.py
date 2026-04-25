"""Template loader for profile and interface-based template selection."""

from __future__ import annotations

import json
from pathlib import Path

from companion.config.loader import get_config


class TemplateLoader:
    """Load prompt templates from config-driven template directories."""

    def __init__(self) -> None:
        self.cfg = get_config()
        self.base_path = Path.cwd()

    def _get_profile_path(self) -> Path:
        templates_cfg = self.cfg["templates"]
        profile = templates_cfg["active_profile"]
        return self.base_path / templates_cfg["profiles"][profile]

    def load(self, name: str) -> dict:
        """Load template from active model profile by name."""
        path = self._get_profile_path() / f"{name}.json"
        return self._load_json(path)

    def load_interface(self, interface: str, name: str) -> dict:
        """Load interface-specific template by name."""
        templates_cfg = self.cfg["templates"]
        path = self.base_path / templates_cfg["interfaces"][interface] / f"{name}.json"
        return self._load_json(path)

    def _load_json(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Template not found: {path}")

        with path.open("r", encoding="utf-8") as file_handle:
            payload = json.load(file_handle)

        if not isinstance(payload, dict):
            raise ValueError(f"Invalid template format: {path}")

        for required_key in ("system", "rules", "template"):
            if required_key not in payload:
                raise ValueError(f"Missing key '{required_key}' in template: {path}")

        return payload
