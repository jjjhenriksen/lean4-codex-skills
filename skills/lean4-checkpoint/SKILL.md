---
name: lean4-checkpoint
description: "Use when the user wants a Lean save point, build-checked checkpoint, scoped staging/commit guidance, axiom/sorry audit, or a final verification gate before committing Lean work."
---

# Lean 4 Checkpoint

Use this skill for a deliberate Lean checkpoint after meaningful proof or code progress.

## Setup

In a workspace with the vendored plugin:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

Relevant upstream docs:

- `vendor/lean4-plugin/commands/checkpoint.md`
- `vendor/lean4-plugin/skills/lean4/SKILL.md`

## Workflow

1. Identify files touched in the current session.
2. Run narrow file checks first: `lake env lean <file>` for touched Lean files.
3. Run `lake build` as the project gate.
4. Audit sorries and axioms using bundled scripts if available.
5. Stage or commit only if the user asked, and only the files touched in this session.

## Useful Prompts

- "Run a Lean checkpoint."
- "Verify this Lean work before we commit."
- "Check for remaining sorries and nonstandard axioms."

