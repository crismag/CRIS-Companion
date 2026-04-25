"""Application entrypoint for CRIS Companion."""

from companion.interface.cli import run_cli


if __name__ == "__main__":
    raise SystemExit(run_cli())
