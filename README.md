# CRIS-Companion

CRIS-Companion is a lightweight coding assistant scaffold with:

- a CLI entrypoint (`main.py`)
- configurable prompt/templates under `config/templates/`
- an optional UI layer under `ui/`
- a focused test suite under `tests/`

## Quick start

### 1) Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Run from the CLI

```bash
python main.py "Summarize the repository architecture"
```

Write output to a file:

```bash
python main.py --output output.md "Draft a release note from recent changes"
```

## Configuration

Runtime settings are loaded from `config/config.yaml`, and prompt/provider templates live in `config/templates/`.

## Development

Run tests:

```bash
pytest -q
```

Helpful docs for extending the project:

- `docs/ARCHITECTURE.md`
- `docs/CODING_GUIDELINES.md`
- `docs/WORKFLOW_CONTRACT.md`
