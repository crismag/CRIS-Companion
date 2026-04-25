"""Repository context loading utilities."""

from __future__ import annotations

from pathlib import Path


def load_context(repo_path: str = ".") -> dict:
    """Load lightweight repository context for prompt construction."""
    root = Path(repo_path)
    python_files = sorted(
        str(path.relative_to(root))
        for path in root.rglob("*.py")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    )
    return {"repo_path": str(root), "python_files": python_files[:50]}
