"""Result display component for Streamlit control plane."""

from __future__ import annotations

import json

import streamlit as st


def _render_response_content(response_text: str) -> None:
    """Render response text as markdown or code based on content."""
    if "```" in response_text:
        st.markdown(response_text)
        return

    st.code(response_text, language="python")


def render_result(result: dict | None) -> None:
    """Render final result payload."""
    if not result:
        st.caption("No result yet.")
        return

    response_text = str(result.get("response", "")).strip()

    if response_text:
        _render_response_content(response_text)

    with st.expander("Raw Result Payload", expanded=False):
        st.code(json.dumps(result, indent=2), language="json")
