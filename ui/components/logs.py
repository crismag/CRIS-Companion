"""Logs display component for Streamlit control plane."""

from __future__ import annotations

import html

import streamlit as st


def _logs_to_text(logs: list[str]) -> str:
    """Convert logs list into display text."""
    return "\n".join(logs)


def _render_scrollable_logs(
    container: st.delta_generator.DeltaGenerator,
    logs_text: str,
) -> None:
    """Render logs in a fixed-height scrollable container."""
    escaped_text = html.escape(logs_text)
    container.markdown(
        (
            "<div style='height:260px; overflow-y:auto; border:1px solid #e0e0e0; "
            "padding:0.5rem; border-radius:0.25rem; background:#0f1116;'>"
            f"<pre style='margin:0; white-space:pre-wrap;'>{escaped_text}</pre>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def create_logs_placeholder() -> st.delta_generator.DeltaGenerator:
    """Create a placeholder container for incremental log streaming."""
    return st.empty()


def update_logs_display(
    logs_placeholder: st.delta_generator.DeltaGenerator,
    logs: list[str],
) -> None:
    """Incrementally render logs into provided placeholder."""
    if not logs:
        logs_placeholder.caption("No logs yet.")
        return

    _render_scrollable_logs(logs_placeholder, _logs_to_text(logs))


def render_logs(logs: list[str]) -> None:
    """Render current execution logs."""
    if not logs:
        st.caption("No logs yet.")
        return

    _render_scrollable_logs(st.container(), _logs_to_text(logs))
