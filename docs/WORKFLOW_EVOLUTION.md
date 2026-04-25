# Workflow Evolution Plan

## Current Model

Single-pass execution:
Task → Prompt → LLM → Output

---

## Target Model (Controlled Loop)

Task → Phase Engine:

1. Module Selection
2. Prompt Construction
3. Generation
4. Validation (optional)
5. Refactor (optional)
6. Completion or Next Step

---

## Key Design Constraint

The workflow loop must be:

- optional (config-driven)
- lightweight (no heavy agent system)
- deterministic (no uncontrolled recursion)

---

## Execution Modes

`config.yaml`:

```yaml
workflow:
  mode: single_pass | iterative
  max_iterations: 3
  enable_refactor: false
```

---

## Principles

- Default remains single-pass
- Loop is opt-in
- Each phase is explicit
- Logging must reflect phase transitions
