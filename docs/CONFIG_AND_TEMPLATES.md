# Configuration and Template System

## Configuration Layers

1. YAML (`config.yaml`)

   - runtime settings
   - model config
   - feature flags

2. JSON Templates

   - prompts
   - messaging formats
   - interface contracts

---

## Template Types

### Model Profiles

- `deepseek/`
- `codellama/`
- `default/`

### Interfaces

- `cli/`
- `rest/`
- `vscode/`

---

## Template Structure

Each template must define:

- `system`: system-level instruction
- `rules`: list of constraints
- `template`: prompt format string

Example:

```json
{
  "system": "...",
  "rules": ["...", "..."],
  "template": "Task:\n{task}\n\nOutput:"
}
```

---

## Rules

- Templates must NOT contain logic
- Templates must be reusable
- Templates must be replaceable via config
- Template selection is dynamic

---

## Template Selection Flow

1. Load active profile from `config.yaml`
2. Load template from corresponding directory
3. Apply interface override if needed

---

## Future Extensions

- A/B template testing
- Runtime switching
- Agent-controlled template selection
