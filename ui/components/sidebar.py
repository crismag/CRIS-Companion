"""Sidebar controls for the Streamlit control plane."""

from __future__ import annotations

import json

import streamlit as st


def _model_options(settings: dict) -> list[str]:
    """Build model options list from current config settings."""
    options: list[str] = []

    primary_model = settings["primary_model"]
    fallback_model = settings["fallback_model"]

    if primary_model:
        options.append(primary_model)

    if fallback_model and fallback_model not in options:
        options.append(fallback_model)

    return options


def render_sidebar(settings: dict) -> dict:
    """Render sidebar controls and return selected values."""
    st.sidebar.header("Control Panel")

    model_options = _model_options(settings)
    default_model = settings["primary_model"]
    default_index = model_options.index(default_model) if default_model in model_options else 0

    selected_model = st.sidebar.selectbox(
        "Model",
        options=model_options,
        index=default_index,
    )

    enable_refactor = st.sidebar.checkbox("Enable refactor phase", value=False)
    enable_validation = st.sidebar.checkbox("Enable validation phase", value=False)
    output_path = st.sidebar.text_input("Output File Path", value="")

    st.sidebar.caption("Config Preview")
    st.sidebar.code(
        json.dumps(
            {
                "selected_model": selected_model,
                "feature_toggles": {
                    "enable_refactor": enable_refactor,
                    "enable_validation": enable_validation,
                },
                "output_path": output_path or None,
            },
            indent=2,
        ),
        language="json",
    )

    return {
        "model_override": selected_model,
        "output_path": output_path.strip(),
        "feature_toggles": {
            "enable_refactor": enable_refactor,
            "enable_validation": enable_validation,
        },
    }
