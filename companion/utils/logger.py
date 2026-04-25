"""Logging helpers for CRIS Companion."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Create or return a configured logger with a predictable format."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger
