"""Configuration loader for CRIS Companion."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

CONFIG_PATH_ENV = "CRIS_CONFIG_PATH"
DEFAULT_CONFIG_PATH = "config/config.yaml"


def _read_config_file(path: Path) -> dict:
    """Read configuration file from disk."""
    import yaml

    with path.open("r", encoding="utf-8") as file_handle:
        parsed = yaml.safe_load(file_handle)
    if not isinstance(parsed, dict):
        raise ValueError(f"Invalid configuration file '{path}': root object must be a mapping.")
    return parsed


def load_config_file(path: str | Path) -> dict:
    """Load a YAML config file from an explicit path."""
    return _read_config_file(Path(path))


@lru_cache(maxsize=1)
def get_config() -> dict:
    """Load and cache project configuration from config file."""
    config_path = Path(os.getenv(CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH))
    config_data = _read_config_file(config_path)

    if not isinstance(config_data.get("llm"), dict):
        raise ValueError("Invalid config: missing llm section")

    if not isinstance(config_data.get("templates"), dict):
        raise ValueError("Invalid config: missing templates section")

    if not isinstance(config_data.get("messages"), dict):
        raise ValueError("Invalid config: missing messages section")

    if not isinstance(config_data.get("workflow"), dict):
        raise ValueError("Invalid config: missing workflow section")

    return config_data


def load_settings() -> dict:
    """Return runtime settings from centralized config."""
    cfg = get_config()
    llm = cfg["llm"]
    messages = cfg["messages"]
    workflow = cfg["workflow"]
    return {
        "ollama_url": llm["ollama_url"],
        "primary_model": llm["primary_model"],
        "fallback_model": llm["fallback_model"],
        "request_timeout_seconds": llm["request_timeout_seconds"],
        "templates": cfg["templates"],
        "messages": messages,
        "workflow": workflow,
    }
