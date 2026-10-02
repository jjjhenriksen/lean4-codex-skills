---
name: lean4-doctor
description: "Use when Lean, Lake, Mathlib, elan, the Lean toolchain, plugin scripts, imports, build configuration, or the local Lean environment is broken or needs diagnosis."
---

# Lean 4 Doctor

Use this skill to diagnose Lean project and environment problems.

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

- `$LEAN4_PLUGIN_ROOT/commands/diagnose.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/SKILL.md`

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
for lake_config in lakefile.lean lakefile.toml; do
  if test -f "$lake_config"; then
    printf '%s\n' "$lake_config"
    sed -n '1,160p' "$lake_config"
  fi
done
```

Inspect whichever configuration exists. If both exist, report both and
identify the active configuration from Lake's behavior instead of assuming
one from the file names. If neither exists, report the missing project
configuration before proposing a repair. Read further relevant sections when
the first 160 lines do not include the needed dependency or library settings.
For TOML projects, inspect `[[require]]` entries and revisions, `[[lean_lib]]`
names, `srcDir` and module roots/globs, alongside `lean-toolchain` and an
existing `lake-manifest.json`. Match module names to actual source paths;
configuration evidence should precede dependency updates or file changes.

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


## TOML import-resolution example

The bundled `examples/toml-import` beside this skill has only `lakefile.toml`,
a pinned Lean toolchain and local source files. Copy it to a temporary workspace
before changing it. The intentionally wrong `srcDir = "MissingSource"` leaves
`DoctorFixture.Basic` unresolved when running:

```bash
lake env lean Src/DoctorFixture.lean
```

The diagnostic block above prints the TOML library settings despite the absence
of `lakefile.lean`. Compare them with `Src/DoctorFixture/Basic.lean`: the source
root is `Src`, so change `srcDir` to `"Src"` in the copied fixture, run
`lake build`, then rerun the file check. The build and import check now succeed
without adding a dependency or downloading Mathlib. A missing import alone
does not establish a missing package; this case is a local source-path error.

The pack's `python3 -m unittest discover -s tests -v` regression executes the
actual documented diagnostic, checks that its TOML evidence is visible, and
reproduces the native failure-to-success transition in an isolated project.
