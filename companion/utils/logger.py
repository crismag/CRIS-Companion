"""Logging helpers for CRIS Companion."""

from __future__ import annotations

import logging


def configure_root_logger(level: int, fmt: str, datefmt: str | None = None) -> None:
    """Configure the root logger with the given level and format.

    Called once at startup (e.g., from ``_configure_logging`` in the CLI) so
    that every module logger — which propagates to root by default — inherits
    the settings from ``config.yaml``. Replaces any existing root handlers so
    a second call (e.g., in tests) always produces the intended configuration.
    """
    root = logging.getLogger()
    root.setLevel(level)

    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(fmt, datefmt=datefmt)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger that propagates to the root logger.

    Format and level are governed by the root logger, which is configured via
    ``configure_root_logger`` (called once at CLI startup from
    ``_configure_logging``).  This ensures that the settings in ``config.yaml``
    are actually applied rather than being shadowed by a private per-module
    handler.
    """
    return logging.getLogger(name)
