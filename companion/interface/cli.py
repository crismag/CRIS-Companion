"""CLI entrypoint for CRIS Companion."""

from __future__ import annotations

import sys

from companion.config.loader import load_settings
from companion.core.engine import run_engine
from companion.interface.formatter import format_output


def run_cli(argv: list[str] | None = None) -> int:
    """Run CRIS Companion from command-line arguments.

    Supported usage:
    - cris "<task>"
    - cris --output <file_path> "<task>"
    """
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        print('Usage: cris [--output <file_path>] "<task>"')
        return 1

    output_path = None

    if len(args) >= 3 and args[0] == "--output":
        output_path = args[1]
        args = args[2:]

    if not args:
        print('Usage: cris [--output <file_path>] "<task>"')
        return 1

    task = " ".join(args)
    settings = load_settings()
    result = run_engine(task, settings, output_path=output_path)
    print(format_output(result))
    return 0
