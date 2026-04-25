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

import yaml

from ui.adapter import EngineAdapter


def _configure_logging(config_path: str = "config.yaml") -> None:
    try:
        with open(config_path, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh)
        log_cfg = cfg.get("logging", {})
        level = getattr(logging, log_cfg.get("level", "INFO"), logging.INFO)
        fmt = log_cfg.get("format", "%(asctime)s [%(levelname)s] %(name)s — %(message)s")
        datefmt = log_cfg.get("datefmt", "%Y-%m-%dT%H:%M:%S")
    except FileNotFoundError:
        level = logging.INFO
        fmt = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"
        datefmt = "%Y-%m-%dT%H:%M:%S"

    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)


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
    if args.command == "review":
        with open(args.file, encoding="utf-8") as fh:
            code = fh.read()
        context = {"code": code}
        task_type = "review"

    elif args.command == "generate":
        context = {"description": args.description, "language": args.language}
        task_type = "generate"

    elif args.command == "refactor":
        with open(args.file, encoding="utf-8") as fh:
            code = fh.read()
        context = {"code": code}
        task_type = "refactor"

    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    response = adapter.run_task(task_type=task_type, context=context)

    if response["status"] == "ok":
        print(response["result"])
        return 0
    else:
        print(f"Error: {response['error']}", file=sys.stderr)
        return 1


def main() -> None:
    _configure_logging()
    parser = _build_parser()
    args = parser.parse_args()
    adapter = EngineAdapter()
    sys.exit(_run(args, adapter))


if __name__ == "__main__":
    main()
