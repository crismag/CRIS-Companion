---
name: generative-coding-standards-skill
description: Use this skill when generating or reviewing code for AI-assisted development to ensure it follows clean code principles, high readability, maintainability, and passes standard linting like flake8.
---

# Purpose

This skill enforces **senior-level coding standards** for AI-generated or AI-assisted code (e.g., using CodeLlama, DeepSeek, or similar tools).
It ensures the output is:

- Clean, readable, and maintainable
- Lint-compliant (flake8-style)
- Well-documented for **junior developer comprehension**
- Structured for long-term scalability

---

# When to use

Use this skill when:

- Generating code via AI models (CodeLlama, DeepSeek, etc.)
- Reviewing or refining AI-generated code
- Designing a generative coding assistant system
- Enforcing coding standards across a team or project
- Producing production-grade or near-production code

---

# Steps

## 1. Structure Before Implementation

- Break problem into **small, well-named functions**
- Each function should:
  - Do **one thing only**
  - Be ≤ ~30–50 lines when possible
- Prefer **composition over monolithic logic**

---

## 2. Naming Conventions

- Use **explicit, descriptive names**
  - ✅ `calculate_invoice_total`
  - ❌ `calc`, `doStuff`
- Boolean variables must read naturally:
  - `is_valid`, `has_access`, `should_retry`

---

## 3. Readability First

- Code must be understandable by a **junior developer without external explanation**
- Avoid clever tricks or overly compact expressions
- Prefer clarity over brevity

---

## 4. Documentation Requirements

### A. Module-Level Docstring

At the top of every file:

```python
"""
Module: invoice_calculator

This module handles invoice total calculations, including tax and discounts.

Designed for clarity and maintainability. Functions are intentionally explicit
to support junior developers and AI-assisted extensions.
"""
```

---

### B. Function-Level Docstrings

Every function must include:

```python
def calculate_total(items, tax_rate):
    """
    Calculate the total price including tax.

    Args:
        items (list[float]): List of item prices.
        tax_rate (float): Tax rate as a decimal (e.g., 0.1 for 10%).

    Returns:
        float: Final total including tax.

    Notes:
        - Assumes all prices are non-negative
        - Does not handle currency formatting
    """
```

---

### C. Inline Comments (Explain WHY, not WHAT)

- Explain reasoning, not obvious operations

```python
# Apply tax after summing to avoid rounding errors per item
total_with_tax = subtotal * (1 + tax_rate)
```

---

## 5. Flake8 Compliance (Strict)

Ensure code passes:

- Line length ≤ 88–100 chars
- No unused imports
- No unused variables
- Proper spacing and formatting
- Consistent indentation (4 spaces)

Avoid:

- Wildcard imports (`from x import *`)
- Deep nesting (>3 levels)

---

## 6. Complexity Management

- Max nesting depth: **3 levels**
- Replace nested conditionals with:
  - Early returns
  - Guard clauses

### Example

❌ Bad:

```python
if user:
    if user.is_active:
        if user.has_permission:
            process()
```

✅ Good:

```python
if not user:
    return

if not user.is_active:
    return

if not user.has_permission:
    return

process()
```

---

## 7. Error Handling

- Use **explicit error handling**
- Avoid silent failures

```python
if not items:
    raise ValueError("items list cannot be empty")
```

---

## 8. Consistency Rules

- One style per project
- One responsibility per function
- Predictable structure across files

---

## 9. AI-Generated Code Refinement Loop

When using CodeLlama / DeepSeek:

1. Generate initial code
2. Apply this checklist:
   - Rename unclear variables
   - Add docstrings
   - Simplify logic
   - Reduce nesting
3. Run linting mentally (flake8-style)
4. Add explanations for non-obvious logic

---

## 10. Output Quality Standard

Final code must:

- Be readable without explanation
- Include full documentation
- Follow consistent style
- Be easy to extend or refactor

---

# Examples

## Example: Clean Function

```python
def filter_active_users(users):
    """
    Filter and return only active users.

    Args:
        users (list[User]): List of user objects.

    Returns:
        list[User]: Active users only.

    Notes:
        - Assumes User has attribute `is_active`
    """
    if not users:
        return []

    active_users = []

    for user in users:
        # Only include users explicitly marked as active
        if user.is_active:
            active_users.append(user)

    return active_users
```

---

## Example: Poor vs Improved

❌ Poor:

```python
def f(x):
    return [i for i in x if i.a]
```

✅ Improved:

```python
def filter_items_with_attribute(items):
    """
    Return items where attribute 'a' is truthy.

    Args:
        items (list[object]): List of objects with attribute 'a'.

    Returns:
        list[object]: Filtered list.
    """
    if not items:
        return []

    filtered_items = []

    for item in items:
        # Keep only items where attribute 'a' is truthy
        if getattr(item, "a", False):
            filtered_items.append(item)

    return filtered_items
```

---

# Key Principle

> Code is not just for machines to execute — it is for humans to understand, maintain, and extend.

This skill prioritizes **clarity over cleverness**, **structure over speed**, and **long-term maintainability over short-term output**.

---

## CRIS Companion Execution Constraints (Project-Specific)

When working in this repository, follow these architectural constraints.

### Current Runtime Mode

The system is currently in **structured single-pass mode** with explicit phases:

`select_module → build_prompt → generate → refactor → return`

### Must-Follow Rules

- DO NOT introduce loops or recursion
- DO NOT implement task queues
- DO NOT add multi-step orchestration
- DO NOT change existing execution behavior

### Allowed Improvements

- improve phase structure
- improve logging
- improve clarity of data flow
- prepare for future extension (without activating it)

### System Constraints

- All config must come from `config.yaml`
- All prompts must come from template JSON files
- No hardcoded values
- UI must remain separate from logic
