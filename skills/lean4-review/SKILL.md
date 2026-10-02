---
name: lean4-review
description: "Use when the user wants a read-only Lean proof review, proof simplification, Mathlib leverage suggestions, refactoring, or proof golfing. Covers lean4 review, refactor, and golf."
---

# Lean 4 Review

Use this skill to inspect Lean code quality, proof robustness, possible simplifications, and opportunities to use Mathlib better.

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

- `$LEAN4_PLUGIN_ROOT/commands/review.md`
- `$LEAN4_PLUGIN_ROOT/commands/refactor.md`
- `$LEAN4_PLUGIN_ROOT/commands/golf.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/SKILL.md`

## Modes

- Review: read-only findings about correctness risk, style, assumptions, and missing checks.
- Refactor: improve proof strategy or extract helper lemmas, with validation.
- Golf: shorten or simplify compiled proofs after correctness is already established.

## Workflow

1. For "review", stay read-only and lead with findings.
2. For "refactor" or "golf", edit only after the user asks for changes.
3. Check for sorries, nonstandard axioms, fragile theorem statements, and avoidable manual proof work.
4. Validate changed Lean files with `lake env lean <file>` and, when appropriate, `lake build`.

## Useful Prompts

- "Use Lean review mode on this file."
- "Refactor this proof to use Mathlib better."
- "Golf this proof, but keep it readable."

