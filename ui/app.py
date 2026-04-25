"""Streamlit Control Plane app for CRIS Companion."""

from __future__ import annotations

from typing import Callable

import streamlit as st

from companion.config.loader import load_settings
from ui.components.controls import render_task_controls
from ui.components.logs import create_logs_placeholder, render_logs, update_logs_display
from ui.components.results import render_result
from ui.components.sidebar import render_sidebar
from ui.services.engine_adapter import execute_task
from ui.state.session import (
    append_log,
    initialize_session_state,
    reset_logs,
    set_result,
    set_status,
)


def _build_log_callback(
    logs_placeholder: st.delta_generator.DeltaGenerator,
) -> Callable[[str], None]:
    """Create callback that appends and renders logs incrementally."""

    def on_log(log_line: str) -> None:
        append_log(log_line)
        update_logs_display(logs_placeholder, st.session_state["logs"])

    return on_log


def _run_execution(task_input: str, controls: dict, settings: dict) -> None:
    """Run one execution cycle through the engine adapter."""
    set_status("running")
    set_result(None)
    reset_logs()

    logs_placeholder = create_logs_placeholder()
    on_log = _build_log_callback(logs_placeholder)

    result = execute_task(
        task=task_input,
        settings=settings,
        output_path=controls.get("output_path") or None,
        model_override=controls.get("model_override") or None,
        on_log=on_log,
    )

    set_result(result)
    set_status("completed")


def _render_main_panel() -> None:
    """Render status, logs, and result sections."""
    st.subheader("Execution Status")
    st.info(st.session_state["status"])

    st.subheader("Logs")
    render_logs(st.session_state["logs"])

    st.subheader("Result")
    render_result(st.session_state.get("result"))


def main() -> None:
    """Render and run the CRIS Companion control plane."""
    st.set_page_config(page_title="CRIS Companion Control Plane", layout="wide")
    st.title("CRIS Companion – Control Plane")

    initialize_session_state()
    settings = load_settings()
    controls = render_sidebar(settings)
    task_input, run_clicked = render_task_controls()

    if run_clicked and task_input.strip():
        _run_execution(task_input, controls, settings)

    _render_main_panel()


if __name__ == "__main__":
    main()
