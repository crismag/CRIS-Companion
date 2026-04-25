"""CLI entrypoint for CRIS Companion."""

from __future__ import annotations

import sys

from companion.config.loader import load_settings
from companion.core.engine import run_engine
from companion.interface.formatter import format_output


def _usage() -> str:
    """Return CLI usage string."""
    return 'Usage: cris [--output <file_path>] "<task>"'


def _parse_arguments(argv: list[str]) -> tuple[str | None, str] | None:
    """Parse output path and task text from CLI arguments."""
    if not argv:
        return None

    output_path = None
    args = list(argv)

    if len(args) >= 3 and args[0] == "--output":
        output_path = args[1]
        args = args[2:]

    if not args:
        return None

    return output_path, " ".join(args)


def run_cli(argv: list[str] | None = None) -> int:
    """Run CRIS Companion from command-line arguments.

    Supported usage:
    - cris "<task>"
    - cris --output <file_path> "<task>"
    """
    parsed = _parse_arguments(list(sys.argv[1:] if argv is None else argv))
    if parsed is None:
        print(_usage())
        return 1

    output_path, task = parsed
    settings = load_settings()
    result = run_engine(task, settings, output_path=output_path)
    print(format_output(result))
    return 0
