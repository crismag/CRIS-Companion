"""Main execution controls for task input and run action."""

from __future__ import annotations

import streamlit as st


def render_task_controls() -> tuple[str, bool]:
    """Render task input and run button."""
    task_input = st.text_area("Task Input", height=140, key="task_input")
    run_clicked = st.button("Run", type="primary")
    return task_input, run_clicked
