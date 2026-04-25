#!/usr/bin/env python3
"""CRIS Companion CLI — end-to-end single-pass engine entry point.

Usage examples
--------------
# Review code in a file
cris review --file mymodule.py

# Generate code from a description
cris generate --description "A function that reverses a list" --language python

# Refactor code in a file
cris refactor --file mymodule.py
"""
import argparse
import logging
import sys

from companion.config.loader import load_config_file
from companion.utils.logger import get_logger

from ui.adapter import EngineAdapter

logger = get_logger(__name__)


def _configure_logging(config_path: str = "config.yaml") -> None:
    try:
        cfg = load_config_file(config_path)
        log_cfg = cfg["logging"]
        level = getattr(logging, log_cfg["level"])
        fmt = log_cfg["format"]
        datefmt = log_cfg["datefmt"]
        logging.basicConfig(level=level, format=fmt, datefmt=datefmt)
    except FileNotFoundError:
        print(
            f"FATAL: Configuration file '{config_path}' was not found.\n"
            "CRIS Companion requires a valid 'config.yaml' to run. "
            "Please complete the setup step to generate or restore this file before using the CLI.",
            file=sys.stderr,
        )
        sys.exit(1)
    except (KeyError, AttributeError, ValueError) as exc:
        print(
            f"FATAL: Configuration error in '{config_path}': {exc}\n"
            "Please check your 'config.yaml' and ensure all required logging settings "
            "(level, format, datefmt) are present and correct.",
            file=sys.stderr,
        )
        sys.exit(1)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cris",
        description="CRIS Companion — AI-assisted code development tool",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # review sub-command
    review = subparsers.add_parser("review", help="Review code for quality and issues")
    review.add_argument("--file", required=True, help="Path to the file to review")

    # generate sub-command
    generate = subparsers.add_parser("generate", help="Generate code from a description")
    generate.add_argument("--description", required=True, help="What the code should do")
    generate.add_argument("--language", default="python", help="Target programming language")

    # refactor sub-command
    refactor = subparsers.add_parser("refactor", help="Suggest refactoring improvements")
    refactor.add_argument("--file", required=True, help="Path to the file to refactor")

    return parser


def _run(args: argparse.Namespace, adapter: EngineAdapter) -> int:
    """Dispatch parsed CLI arguments to the adapter and print the result."""
    task = _resolve_task(args)
    if task is None:
        logger.error("Unknown command: %s", args.command)
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    task_type, context = task
    response = adapter.run_task(task_type=task_type, context=context)

    if response["status"] == "ok":
        print(response["result"])
        return 0
    else:
        logger.error("Command failed: %s", response["error"])
        print(f"Error: {response['error']}", file=sys.stderr)
        return 1


def _read_text_file(path: str) -> str:
    """Read and return UTF-8 text file contents."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _resolve_task(args: argparse.Namespace) -> tuple[str, dict] | None:
    """Map CLI arguments to (task_type, context)."""
    if args.command == "review":
        return "review", {"code": _read_text_file(args.file)}

    if args.command == "generate":
        return "generate", {"description": args.description, "language": args.language}

    if args.command == "refactor":
        return "refactor", {"code": _read_text_file(args.file)}

    return None


def main() -> None:
    _configure_logging()
    parser = _build_parser()
    args = parser.parse_args()
    adapter = EngineAdapter()
    sys.exit(_run(args, adapter))


if __name__ == "__main__":
    main()
