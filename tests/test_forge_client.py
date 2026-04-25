"""Tests for Ollama forge client integration."""

from __future__ import annotations

import json
from urllib import error

import pytest

from companion.integration import forge_client


class _FakeResponse:
    """Fake urllib response for unit tests."""

    def __init__(self, payload: dict):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_generate_text_returns_response_body(monkeypatch) -> None:
    """Client should return response text from Ollama payload."""

    def fake_urlopen(http_request, timeout):
        assert http_request.full_url == "http://localhost:11434/api/generate"
        assert timeout == 5
        return _FakeResponse({"response": "print('hello')"})

    monkeypatch.setattr(forge_client.request, "urlopen", fake_urlopen)

    result = forge_client.generate_text(
        "create hello script",
        {
            "ollama_url": "http://localhost:11434",
            "primary_model": "test",
            "request_timeout_seconds": 5,
        },
    )

    assert result == "print('hello')"


def test_generate_text_handles_network_error(monkeypatch) -> None:
    """Client should return clean error message for URLError."""

    def fake_urlopen(http_request, timeout):
        raise error.URLError("connection refused")

    monkeypatch.setattr(forge_client.request, "urlopen", fake_urlopen)

    result = forge_client.generate_text(
        "create hello script",
        {
            "ollama_url": "http://localhost:11434",
            "primary_model": "test",
            "request_timeout_seconds": 5,
        },
    )

    assert "LLM request failed" in result


def test_generate_text_requires_settings() -> None:
    """Client should fail fast when runtime settings are missing."""
    with pytest.raises(ValueError):
        forge_client.generate_text("create hello script")
