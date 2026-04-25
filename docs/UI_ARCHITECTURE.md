# UI Architecture

## Structure

```text
ui/
├── app.py             # main Streamlit app
├── components/
│   ├── sidebar.py
│   ├── logs.py
│   ├── controls.py
│   └── results.py
├── state/
│   └── session.py
└── services/
    └── engine_adapter.py
```

---

## Responsibilities

### app.py

- layout orchestration
- page rendering

### components/*

- reusable UI blocks

### state/session.py

- manages Streamlit session state
- stores logs, results, status

### engine_adapter.py

- interface between UI and Engine
- handles execution calls

---

## Design Rules

- No direct Engine logic inside components
- No LLM calls in UI
- UI communicates via adapter
- Logging must flow through session state

---

## Logging Pattern

Use Python logging + custom handler to stream logs to UI.

Logs must:

- update incrementally
- persist during session
- avoid duplication due to reruns

---

## State Handling

Use `st.session_state` for:

- logs
- current task
- execution status
- result
