---
name: lean4-prove
description: "Use when the user wants to fill Lean sorries, prove an existing theorem, repair a failing Lean proof, debug tactic errors, or run guided/autonomous proof cycles. Covers lean4 prove and autoprove."
---

# Lean 4 Prove

Use this skill for proof work on existing Lean declarations.

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

- `$LEAN4_PLUGIN_ROOT/commands/prove.md`
- `$LEAN4_PLUGIN_ROOT/commands/autoprove.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/SKILL.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/references/sorry-filling.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/references/cycle-engine.md`

Read the reference files only when the proof is nontrivial or a proof loop is requested.

## Workflow

1. Confirm scope: one sorry, one theorem, one file, or project.
2. Preserve theorem statements and declaration headers unless the user explicitly allows edits.
3. Inspect the goal/error, then search local code and Mathlib before inventing a proof.
4. Add helper lemmas only when they clarify the proof or are needed repeatedly.
5. Validate narrowly with `lake env lean <file>`, then broader with `lake build` if appropriate.

## Stop Conditions

Stop and report clearly if:

- the theorem appears false,
- a statement change seems necessary,
- an axiom would be required,
- repeated proof attempts are stuck on the same blocker.

## Useful Prompts

- "Use Lean prove mode to fill this sorry."
- "Repair this proof without changing the theorem statement."
- "Autoprove the remaining sorries in this file with a small stop budget."

