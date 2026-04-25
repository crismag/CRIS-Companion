"""Factory for runtime text-generation providers."""

from __future__ import annotations

from companion.integration.forge_client import generate_text


class OllamaProvider:
    """Provider adapter that offers a `.generate(prompt)` interface."""

    def __init__(self, settings: dict) -> None:
        self.settings = settings

    def generate(self, prompt: str) -> str:
        return generate_text(prompt, self.settings).strip()


def get_provider(settings: dict):
    """Return provider implementation for current runtime settings."""
    return OllamaProvider(settings)
