---
name: lean4-doctor
description: "Use when Lean, Lake, Mathlib, elan, the Lean toolchain, plugin scripts, imports, build configuration, or the local Lean environment is broken or needs diagnosis."
---

# Lean 4 Doctor

Use this skill to diagnose Lean project and environment problems.

## Setup

In a workspace with the vendored plugin:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

Relevant upstream docs:

- `vendor/lean4-plugin/commands/doctor.md`
- `vendor/lean4-plugin/skills/lean4/SKILL.md`

## Checks

Run the smallest useful set:

```bash
pwd
which elan || true
which lean || true
which lake || true
lean --version
lake --version
test -f lean-toolchain && cat lean-toolchain
test -f lakefile.lean && sed -n '1,160p' lakefile.lean
```

Then try:

```bash
lake build
```

For import or file-specific issues, use:

```bash
lake env lean path/to/File.lean
```

## Useful Prompts

- "Run Lean doctor."
- "Why is Lake failing?"
- "Diagnose this Lean import/toolchain issue."

