"""Simple Ollama client integration for CRIS Companion."""

from __future__ import annotations

import json
from urllib import error, request


def generate_text(prompt: str, settings: dict | None = None) -> str:
    """Send prompt text to Ollama and return response text."""
    if not settings:
        raise ValueError("Missing runtime settings for LLM client")

    ollama_url = settings["ollama_url"]
    model = settings["primary_model"]
    timeout_seconds = settings["request_timeout_seconds"]
    endpoint = f"{ollama_url.rstrip('/')}/api/generate"

    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
    ).encode("utf-8")

    http_request = request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        return f"LLM request failed: {exc.reason}"
    except TimeoutError:
        return "LLM request failed: timeout"
    except json.JSONDecodeError:
        return "LLM request failed: invalid JSON response"

    return str(body.get("response", "")).strip()
