# CRIS Companion – Workflow Discipline Status

## Overview

The system currently operates in a **single-pass execution model**:

Task → Prompt → LLM → Result

This remains the active runtime model and is still aligned with MVP constraints.

---

## Progress Comparison (Previous vs Current)

| Workflow Step | Previous Status | Current Status | Progress |
|---|---|---|---|
| 1. Select Module | NOT IMPLEMENTED | PARTIALLY IMPLEMENTED | Added explicit `select_module()` phase (currently fixed to `coding`). |
| 2. Use System Prompt | IMPLEMENTED | IMPLEMENTED | No change; template-driven prompt construction remains in place. |
| 3. Generate Code | IMPLEMENTED | IMPLEMENTED | No change; engine generation path remains stable. |
| 4. Run Locally | PARTIALLY IMPLEMENTED | IMPLEMENTED | Available through CLI and Streamlit control plane execution path. |
| 5. Refactor Using Sweep Prompt | NOT IMPLEMENTED | PARTIALLY IMPLEMENTED | Added explicit `refactor()` phase as non-mutating stub. |
| 6. Move to Next Module | NOT IMPLEMENTED | NOT IMPLEMENTED | No loop or queue orchestration yet. |

---

## Workflow Steps Status (Current)

### 1. Select Module

Status: PARTIALLY IMPLEMENTED

- Engine has explicit `select_module()` phase
- Current module choice is static (`coding`)
- No dynamic decomposition/planning yet

---

### 2. Use System Prompt

Status: IMPLEMENTED

- Templates loaded via `TemplateLoader`
- Prompt rendered from `system + rules + template`
- No inline prompt embedding in UI

---

### 3. Generate Code

Status: IMPLEMENTED

- Engine builds prompt
- LLM client calls Ollama API
- Structured result returned

---

### 4. Run Locally

Status: IMPLEMENTED

- CLI path available for local execution
- Streamlit control plane path available for local execution
- Automated tests run in local development workflow

---

### 5. Refactor Using Sweep Prompt

Status: PARTIALLY IMPLEMENTED

- Explicit `refactor()` phase exists
- Current behavior is pass-through (no transformation)
- Designed as extension point for future iterations

---

### 6. Move to Next Module

Status: NOT IMPLEMENTED

- No workflow loop or task queue
- No multi-step module progression
- Single-pass execution remains intentional

---

## Current Compliance Snapshot

Current system is:

✔ Config-driven
✔ Template-driven
✔ Single-pass execution
✔ Explicit phase boundaries
✔ Structured phase logging
✔ UI adapter isolation from Engine internals

Still missing:

❌ Iterative workflow loop
❌ Task decomposition engine
❌ Active refactor cycle
❌ Multi-step orchestration

---

## Target Evolution (unchanged)

Phase 1 (current):

- single-pass generation with explicit phase structure

Phase 2:

- introduce optional validation/refactor activation flags

Phase 3:

- introduce iterative refinement loop (config-controlled)

Phase 4:

- introduce module-level orchestration with bounded progression

---

## Design Decision

The workflow loop remains intentionally deferred.

Reason:

- Maintain simplicity
- Validate core generation and observability first
- Avoid premature complexity

Future implementation must:

- be optional
- be controlled via config
- not break existing behavior
