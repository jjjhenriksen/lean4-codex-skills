---
name: lean4-review
description: "Use when the user wants a read-only Lean proof review, proof simplification, Mathlib leverage suggestions, refactoring, or proof golfing. Covers lean4 review, refactor, and golf."
---

# Lean 4 Review

Use this skill to inspect Lean code quality, proof robustness, possible simplifications, and opportunities to use Mathlib better.

## Setup

In a workspace with the vendored plugin:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

Relevant upstream docs:

- `vendor/lean4-plugin/commands/review.md`
- `vendor/lean4-plugin/commands/refactor.md`
- `vendor/lean4-plugin/commands/golf.md`
- `vendor/lean4-plugin/skills/lean4/SKILL.md`

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

