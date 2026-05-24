---
name: lean4-learn
description: "Use when the user wants to learn Lean 4 interactively, explore mathlib or a Lean repository, ask conceptual Lean questions, understand proof states, or use mentor-style Lean onboarding. Covers the lean4 learn workflow."
---

# Lean 4 Learn

Use this skill for Lean learning and exploration. Keep the interaction concrete, exploratory, and Lean-backed when possible.

## Setup

From a Lean workspace that vendors `lean4-plugin`, run commands with:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

If the task is in `/Users/jacquelinehenriksen/Documents/Lean4`, the upstream workflow docs are:

- `vendor/lean4-plugin/commands/learn.md`
- `vendor/lean4-plugin/skills/lean4/SKILL.md`
- `~/.codex/skills/lean4-mentor/references/mentor-orientation.md`

Read only the sections needed for the user’s topic.

## Workflow

1. Resolve intent: repo exploration, mathlib navigation, concept explanation, or exercise.
2. Prefer tiny live examples: `#check`, `#eval`, a small theorem, or a small proof state.
3. If a Lean project exists, validate key claims with `lake env lean <file>` or `lake build`.
4. Do not write files unless the user asks for a scratch/example artifact.
5. End with one natural next experiment, not a long curriculum.

## Useful Prompts

- "Use Lean learn mode to explain this file."
- "Walk me through this theorem state."
- "Help me understand this Mathlib concept with tiny examples."
- "Teach me Lean as an interactive semantic environment."

