"""Task routing for model and action selection."""

from __future__ import annotations

from companion.interface.commands import CommandIntent


def route_task(intent: CommandIntent) -> dict:
    """Route an intent to a simple action plan.

    Keeps routing explicit for MVP behavior.
    """
    if intent.action == "generate_python_file":
        return {"action": "generate_file", "language": "python"}

    if intent.action == "create_file":
        return {"action": "create_file", "language": None}

    return {"action": "chat", "language": None}
