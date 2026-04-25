"""Command parsing for CRIS Companion CLI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CommandIntent:
    """Represent parsed user intent from CLI text."""

    action: str
    file_path: str | None
    prompt: str


def parse_command(raw_input: str) -> CommandIntent:
    """Parse a user command into a structured intent.

    Supported commands:
    - create a python script <file_path>
    - create file <file_path>
    """
    normalized = raw_input.strip()
    lower_text = normalized.lower()

    if lower_text.startswith("create a python script "):
        file_path = normalized[len("create a python script ") :].strip()
        return CommandIntent(
            action="generate_python_file",
            file_path=file_path,
            prompt=normalized,
        )

    if lower_text.startswith("create file "):
        file_path = normalized[len("create file ") :].strip()
        return CommandIntent(action="create_file", file_path=file_path, prompt=normalized)

    return CommandIntent(action="chat", file_path=None, prompt=normalized)
