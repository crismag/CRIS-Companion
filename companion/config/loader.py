"""Configuration loader for CRIS Companion."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

CONFIG_PATH_ENV = "CRIS_CONFIG_PATH"
DEFAULT_CONFIG_PATH = "config/config.yaml"


def _read_config_file(path: Path) -> dict:
    """Read configuration file from disk."""
    content = path.read_text(encoding="utf-8")

    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(content)
        return parsed if isinstance(parsed, dict) else {}
    except ModuleNotFoundError:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, dict) else {}


@lru_cache(maxsize=1)
def get_config() -> dict:
    """Load and cache project configuration from config file."""
    config_path = Path(os.getenv(CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH))
    config_data = _read_config_file(config_path)

    if not isinstance(config_data.get("llm"), dict):
        raise ValueError("Invalid config: missing llm section")

    if not isinstance(config_data.get("templates"), dict):
        raise ValueError("Invalid config: missing templates section")

    return config_data


def load_settings() -> dict:
    """Return runtime settings from centralized config."""
    cfg = get_config()
    llm = cfg["llm"]
    return {
        "ollama_url": llm["ollama_url"],
        "primary_model": llm["primary_model"],
        "fallback_model": llm.get("fallback_model"),
        "request_timeout_seconds": llm["request_timeout_seconds"],
        "templates": cfg["templates"],
        "messages": cfg.get("messages", {}),
        "workflow": cfg.get("workflow", {}),
    }
