"""Session state helpers for Streamlit control plane."""

from __future__ import annotations

import streamlit as st


def initialize_session_state() -> None:
    """Initialize required session state keys."""
    st.session_state.setdefault("logs", [])
    st.session_state.setdefault("status", "idle")
    st.session_state.setdefault("result", None)


def reset_logs() -> None:
    """Reset session logs for a fresh run."""
    st.session_state["logs"] = []


def append_log(log_line: str) -> None:
    """Append log line to session logs while avoiding direct duplicates."""
    logs: list[str] = st.session_state["logs"]

    if logs and logs[-1] == log_line:
        return

    logs.append(log_line)


def set_status(status: str) -> None:
    """Set current execution status in session state."""
    st.session_state["status"] = status


def set_result(result: dict | None) -> None:
    """Set latest execution result in session state."""
    st.session_state["result"] = result
