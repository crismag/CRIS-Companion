# CRIS Companion – Workflow Contract

## Current Execution Model

CRIS Companion operates in **step-based single-pass mode**:

1. build execution step
2. execute step
3. return result

The internal shape is:

Task → Execution Step → Result

This preserves single-pass behavior while making the execution unit explicit.

---

## Critical Constraint

The system MUST NOT:

- introduce loops
- introduce recursion
- introduce task queues
- introduce multi-step planning

unless explicitly enabled via configuration.

---

## Execution Step Contract

Each execution step must include:

- `name`
- `intent`
- `template`
- `inputs`

This step object is the compatibility unit for future graph-based orchestration.

---

## Step Executor Contract

The executor must:

- load a template by step name
- build prompt text from template + step inputs
- call provider through a `.generate(prompt)` interface
- return provider output unchanged

---

## Task Controller Contract

The task controller must:

- deterministically produce a single step from task input
- avoid decomposition/planning in single-pass mode
- remain easy to extend for future multi-step workflows

---

## Logging Contract

- Every engine phase must log phase start events
- Logs must be UI-consumable
- Logs must be deterministic (no duplication)

---

## UI Contract

- UI reflects phases only
- UI does not influence execution logic
- UI must remain a passive observer + trigger

---

## Future Evolution Guardrails

When introducing new capabilities:

- Must be config-gated
- Must preserve single-pass default
- Must not introduce hidden behavior
