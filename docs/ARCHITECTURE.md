# CRIS Companion Architecture

CRIS Companion is the assistant layer of the CRIS platform.

## Responsibilities
- Interpret user intent
- Build execution step from user task
- Load templates and build prompts
- Call provider integration
- Format and present results

## High-Level Flow

User Input → CLI/UI → Engine → TaskController → StepExecutor → Provider → Response

## Key Components

- Engine: main orchestration loop
- TaskController: converts task input into one execution step
- StepExecutor: loads template, builds prompt, calls provider
- TemplateLoader: resolves template payloads from config-selected profile
- Forge Client / Provider Factory: provider integration for text generation
