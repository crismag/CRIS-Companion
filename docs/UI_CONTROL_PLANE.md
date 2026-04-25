# CRIS Companion – Control Plane UI Context

## Purpose

The Control Plane UI provides:

- Task input (prompt submission)
- Execution monitoring (logs + progress)
- Config visibility and control
- Result visualization

This UI is NOT a product UI. It is a developer control interface.

---

## UI Philosophy

- Minimal
- Functional
- Observable
- Real-time feedback
- No heavy frontend framework

---

## Platform Choice

The UI is implemented using Streamlit.

Reasons:

- Python-native
- Fast iteration
- Direct integration with CRIS Companion
- Supports real-time updates and logging

---

## Responsibilities

The UI must:

1. Accept user task input
2. Trigger execution via Engine
3. Display execution progress
4. Display logs in real-time
5. Display final result
6. Allow limited config overrides (non-persistent)

---

## Layout Design

### Sidebar (Control Panel)

- Model selection
- Feature toggles
- Config preview

### Main Panel

- Task input box
- Run button
- Execution status
- Logs output (live)
- Final result

---

## Execution Flow

User → UI → Engine → LLM/Tools → Logs → UI

---

## Logging Requirements

- Logs must be visible in UI
- Logs must be structured
- Logs must not be duplicated on reruns

---

## Progress Requirements

The UI must reflect:

- current step
- execution stage
- completion status

---

## Constraints

- No business logic in UI
- UI must call Engine only
- UI must not call LLM directly
- UI must not contain prompt logic

---

## Future Extensions

- task history
- multi-run comparison
- session tracking
- model benchmarking
- REST control plane

---

## Critical Rules

- UI is a thin layer
- Engine handles logic
- Templates handle prompts
- Config handles behavior
