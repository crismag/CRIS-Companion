# CRIS Companion Architecture

CRIS Companion is the assistant layer of the CRIS platform.

## Responsibilities
- Interpret user intent
- Load relevant context (files, repo)
- Route tasks to CRIS Forge
- Format and present results

## High-Level Flow

User Input → CLI → Engine → Router → Forge Client → LLM/Tools → Response

## Key Components

- Engine: main orchestration loop
- Router: decides which model/tool to use
- Forge Client: communicates with CRIS Forge
- Context Loader: extracts relevant files/code
