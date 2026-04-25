"""Application settings for CRIS Companion."""

from pathlib import Path

import yaml

_FALLBACK_OLLAMA_URL = "http://localhost:11434"
_FALLBACK_PRIMARY_MODEL = "deepseek-coder:6.7b"
_FALLBACK_FALLBACK_MODEL = "codellama:7b"
_FALLBACK_REQUEST_TIMEOUT_SECONDS = 60


def _load_config():
    """Load project configuration from config/config.yaml if present."""
    config_path = Path(__file__).resolve().parents[2] / "config" / "config.yaml"
    if not config_path.is_file():
        return {}

    with config_path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    return data if isinstance(data, dict) else {}


def _get_config_value(config, candidate_paths, default):
    """Return the first configured value found for any candidate path."""
    for path in candidate_paths:
        current = config
        for key in path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if current is not None:
            return current
    return default


_CONFIG = _load_config()

DEFAULT_OLLAMA_URL = _get_config_value(
    _CONFIG,
    (
        ("ollama", "url"),
        ("models", "ollama_url"),
        ("DEFAULT_OLLAMA_URL",),
    ),
    _FALLBACK_OLLAMA_URL,
)
PRIMARY_MODEL = _get_config_value(
    _CONFIG,
    (
        ("models", "primary"),
        ("llm", "primary_model"),
        ("PRIMARY_MODEL",),
    ),
    _FALLBACK_PRIMARY_MODEL,
)
FALLBACK_MODEL = _get_config_value(
    _CONFIG,
    (
        ("models", "fallback"),
        ("llm", "fallback_model"),
        ("FALLBACK_MODEL",),
    ),
    _FALLBACK_FALLBACK_MODEL,
)
REQUEST_TIMEOUT_SECONDS = _get_config_value(
    _CONFIG,
    (
        ("request", "timeout_seconds"),
        ("ollama", "timeout_seconds"),
        ("REQUEST_TIMEOUT_SECONDS",),
    ),
    _FALLBACK_REQUEST_TIMEOUT_SECONDS,
)
