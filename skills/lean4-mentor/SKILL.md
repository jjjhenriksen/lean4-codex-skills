---
name: lean4-mentor
description: "Use when the user wants to learn Lean 4, explore Lean as an interactive semantic environment, set up Lean 4 study/workflows in Codex, debug Lean/lake/mathlib issues, or combine Lean 4 proof tooling with a mentor-style onboarding path. Prefer this over generic theorem-proving help for Lean 4."
---

# Lean 4 Mentor

Use this skill for Lean 4 learning and Lean project work in Codex. It combines:

- the local Lean workflow pack at `vendor/lean4-plugin`, when present in the workspace
- the mentor posture in `references/mentor-orientation.md`
- the upstream Lean 4 skill instructions in `vendor/lean4-plugin/skills/lean4/SKILL.md`

For operational work, prefer the narrower split skills when they match:

- `lean4-learn` for teaching, repo exploration, and mathlib exploration
- `lean4-formalize` for drafting statements and formalizing prose
- `lean4-prove` for filling sorries and repairing proofs
- `lean4-review` for review, refactor, and golf
- `lean4-checkpoint` for build-checked save points
- `lean4-doctor` for environment and toolchain diagnosis

## First Move

1. Check whether the current workspace has `vendor/lean4-plugin`.
2. If present, set these for the session before using bundled scripts:

```bash
export LEAN4_PLUGIN_ROOT="$PWD/vendor/lean4-plugin"
export LEAN4_SCRIPTS="$LEAN4_PLUGIN_ROOT/lib/scripts"
export LEAN4_PYTHON_BIN="${LEAN4_PYTHON_BIN:-python3}"
```

3. If the user is learning Lean, read `references/mentor-orientation.md` and keep the conversation exploratory.
4. If editing or proving Lean, read `vendor/lean4-plugin/skills/lean4/SKILL.md` and follow its safety rules.

## Teaching Posture

Present Lean first as an interactive semantic environment: programming language, specification language, metaprogramming system, executable modeling tool, and proof assistant. Do not make theorem proving the whole story unless the user asks for that lane.

Prefer tiny live experiments:

- inspect inferred types
- change a term and observe the error/goal
- show what elaboration or instance search inferred
- use a small proof state as an interactive transformation, not a lecture
- connect examples to mainstream engineering only when it clarifies the mental model

Avoid long formal explanations, category theory dumps, deep proof theory early, or "Lean is Haskell with proofs" framing.

## Operational Workflow

When the user asks for proof, formalization, or mathlib work, translate Claude-style `/lean4:*` commands into Codex actions:

- `learn`: interactive exploration, read-only by default
- `draft`: create declaration skeletons from informal claims
- `formalize`: draft declarations, then help prove them interactively
- `prove`: fill existing `sorry`s with explicit checkpoints
- `autoprove`: autonomous proof cycles with clear stop budgets
- `review`: read-only quality and safety review
- `doctor`: diagnose Lean, Lake, mathlib, and plugin setup

Use Lean/Lake as the test suite. Validate with the narrowest useful gate first:

```bash
lake env lean path/to/File.lean
lake build
```

Use bundled scripts only through `$LEAN4_SCRIPTS`, never as bare names.

## Safety

- Do not change theorem statements or add axioms without explicit permission.
- Keep Lean lines around 100 characters when editing.
- Use scratch files outside the repo root unless the user asked for a workspace artifact.
- Stage or commit only when the user asks, and only files touched in the current session.
- For learning sessions, stay read-only unless the user asks to create exercises, scratch files, or a project.
