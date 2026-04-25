# Module Contracts

## Engine

Input:

- user task (string)

Responsibilities:

- load config
- load template
- call LLM
- trigger tools

Output:

- structured result

---

## Template Loader

Input:

- template name
- profile

Output:

- structured template dict

---

## LLM Client

Input:

- prompt string

Output:

- generated text

Constraints:

- must use config values
- must not hardcode endpoints

---

## File Tools

Responsibilities:

- controlled file writes
- safe directory creation

Constraints:

- no direct system-level operations
- no unsafe writes

---

## CLI

Responsibilities:

- parse user input
- call engine
- display result

Constraints:

- minimal logic
