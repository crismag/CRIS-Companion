# CRIS Companion – Master Project Context

## Purpose

CRIS Companion is the assistant layer of the CRIS platform.

It provides a Copilot-like developer experience using local AI models via Ollama.

It interprets user intent and delegates execution to underlying systems (initially direct LLM + tools, later CRIS Forge).

## System Architecture

```text
CRIS (Platform)
├── CRIS Forge → execution engine (LLM + tools)
└── CRIS Companion → assistant / orchestration / UX
```

## Responsibilities of CRIS Companion

- Interpret user intent
- Load contextual data (files, repo, configs)
- Build structured prompts using templates
- Call LLM via Ollama
- Perform controlled file operations
- Return structured outputs
- Maintain predictable execution flow

## Configuration Philosophy

CRIS Companion is a config-driven system.

ALL runtime behavior must be controlled via:

- `config/config.yaml`
- `config/templates/*`
- `config/*.json` (structured configs)

No hardcoded values are allowed.

## Template System

Templates are modular and organized by:

- Model profile (deepseek, codellama, default)
- Interface type (cli, rest, vscode)

Templates define:

- system prompts
- rules
- message structures
- output formatting

Templates are treated as configuration, not logic.

## Execution Flow (MVP)

User Input → CLI → Engine → Template Loader → LLM Client → Tool Execution → Output

## Current Scope (MVP)

- CLI interaction
- Code generation
- File writing
- Basic task execution
- Config + template-driven behavior

## Future Scope

- Diff-based editing
- Context-aware repo analysis
- Multi-model routing
- CRIS Forge integration
- VSCode extension
- Agent loop execution

## Design Principles

- Configuration over hardcoding
- Templates over inline prompts
- Simplicity over abstraction
- Explicit flow over hidden behavior
- Modular structure
- Replaceable components
- Deterministic execution

## Non-Goals (for now)

- No full agent loop
- No dynamic plugin framework
- No distributed execution
- No over-abstracted architecture

## Target UX

```bash
cris "create a python file hello.py"
```

System:

- builds prompt from template
- generates code
- writes file
- returns output

## Critical Rules

- NO hardcoded prompts
- NO hardcoded model configs
- NO hardcoded paths
- ALL templates must come from `config/templates`
- ALL config must come from `config.yaml`
