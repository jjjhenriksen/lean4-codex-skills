---
name: lean4-formalize
description: "Use when the user wants to draft Lean declarations from informal math, turn prose into theorem statements, formalize a claim, create skeletons with sorries, or run an end-to-end formalization workflow. Covers lean4 draft, formalize, and autoformalize."
---

# Lean 4 Formalize

Use this skill to turn informal claims into Lean declarations and, when requested, begin proving them.

## Setup

In a workspace with the vendored plugin:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

Relevant upstream docs:

- `vendor/lean4-plugin/commands/draft.md`
- `vendor/lean4-plugin/commands/formalize.md`
- `vendor/lean4-plugin/commands/autoformalize.md`
- `vendor/lean4-plugin/skills/lean4/SKILL.md`

## Workflow

1. Identify the informal claim, assumptions, definitions, and target namespace/file.
2. Draft the Lean statement first. Prefer a skeleton with `sorry` over guessing a brittle proof.
3. Ask before changing mathematical meaning or theorem headers after the statement is accepted.
4. Search local code and Mathlib before inventing definitions.
5. Validate with `lake env lean <file>` after writing declarations.

## Safety

- Do not silently strengthen/weaken a theorem.
- Do not add axioms without explicit permission.
- Keep generated source close to the user’s wording unless Mathlib naming requires a change.

## Useful Prompts

- "Use Lean formalize mode for this claim."
- "Draft theorem skeletons for these statements."
- "Autoformalize this paragraph into Lean declarations."

