# Lean 4 Codex Skills

Small Codex skill pack for Lean 4 work.

This repository splits a broad Lean 4 workflow into narrower Codex skills:

- `lean4-mentor` — front-door orientation for learning Lean as an interactive semantic environment
- `lean4-learn` — teaching, repo exploration, and mathlib exploration
- `lean4-formalize` — draft/formalize/autoformalize workflows
- `lean4-prove` — proving existing declarations, filling sorries, and proof repair
- `lean4-review` — review, refactor, and proof golfing
- `lean4-checkpoint` — build-checked save points and sorry/axiom audits
- `lean4-doctor` — Lean/Lake/toolchain diagnosis

The skills are intentionally thin. They are designed to point Codex toward the
right Lean workflow without loading a large monolithic instruction file every
time.

## Install

Copy the skill folders into your Codex skills directory:

```bash
cp -R skills/lean4-* ~/.codex/skills/
```

Then start a new Codex session so the skills are discovered.

## Recommended Workspace Setup

For best results, use these skills in a Lean workspace that has:

- `lean-toolchain`
- `lakefile.lean` or `lakefile.toml`
- working `lean` and `lake` commands, usually through `elan`

The skills can also use a vendored copy of Cameron Freer's `lean4-skills`
workflow pack if the workspace contains:

```text
vendor/lean4-plugin/
```

and an env file like:

```bash
export LEAN4_PLUGIN_ROOT="$PWD/vendor/lean4-plugin"
export LEAN4_SCRIPTS="$LEAN4_PLUGIN_ROOT/lib/scripts"
export LEAN4_PYTHON_BIN="${LEAN4_PYTHON_BIN:-python3}"
```

## Example Prompts

```text
Use lean4-learn to explain this proof state.
```

```text
Use lean4-prove to fill the sorry in MergeSort.lean without changing the theorem statement.
```

```text
Use lean4-review on this file and lead with correctness risks.
```

```text
Run lean4-doctor and diagnose why Lake is failing.
```

## Notes

These skills were adapted for Codex from two sources:

- Pavel's Lean mentor orientation prompt
- Cameron Freer's `lean4-skills` workflow structure

They do not vendor the full upstream Lean workflow pack. If you want the
scripts and full command references, add that repository separately under your
Lean workspace.

