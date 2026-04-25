"""Output formatting for CLI responses."""

from __future__ import annotations


def format_output(result: dict) -> str:
    """Format engine result for terminal output."""
    status = result.get("status", "unknown")
    message = result.get("message", "")
    file_path = result.get("file_path")

    if file_path:
        return f"[{status}] {message}: {file_path}"

    return f"[{status}] {message}"
