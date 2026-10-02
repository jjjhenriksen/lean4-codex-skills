---
name: lean4-formalize
description: "Use when the user wants to draft Lean declarations from informal math, turn prose into theorem statements, formalize a claim, create skeletons with sorries, or run an end-to-end formalization workflow. Covers lean4 draft, formalize, and autoformalize."
---

# Lean 4 Formalize

Use this skill to turn informal claims into Lean declarations and, when requested, begin proving them.

## Setup

Resolve the optional plugin root for this workspace. An existing
`lean4-codex.env` is loaded first; unset variables use the documented defaults:

```bash
if test -f ./lean4-codex.env; then
  source ./lean4-codex.env
fi
export LEAN4_PLUGIN_ROOT="${LEAN4_PLUGIN_ROOT:-$PWD/vendor/lean4-plugin}"
export LEAN4_SCRIPTS="${LEAN4_SCRIPTS:-$LEAN4_PLUGIN_ROOT/lib/scripts}"
export LEAN4_PYTHON_BIN="${LEAN4_PYTHON_BIN:-python3}"
```

Resolve each reference below against `$LEAN4_PLUGIN_ROOT`, preserving spaces
in the path. Check for each file before reading it; report and skip absent
optional guidance, then continue the native workflow. The skill remains usable
without a plugin. Use scripts only via the resolved `$LEAN4_SCRIPTS`.

Relevant upstream docs:

- `$LEAN4_PLUGIN_ROOT/commands/draft.md`
- `$LEAN4_PLUGIN_ROOT/commands/formalize.md`
- `$LEAN4_PLUGIN_ROOT/commands/autoformalize.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/SKILL.md`

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

