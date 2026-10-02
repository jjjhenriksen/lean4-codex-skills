---
name: lean4-checkpoint
description: "Use when the user wants a Lean save point, build-checked checkpoint, scoped staging/commit guidance, axiom/sorry audit, or a final verification gate before committing Lean work."
---

# Lean 4 Checkpoint

Use this skill for a deliberate Lean checkpoint after meaningful proof or code progress.

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

- `$LEAN4_PLUGIN_ROOT/commands/checkpoint.md`
- `$LEAN4_PLUGIN_ROOT/skills/lean4/SKILL.md`

## Workflow

1. Identify files touched in the current session.
2. Run narrow file checks first: `lake env lean <file>` for touched Lean files.
3. Run `lake build` as the project gate.
4. Run the native sorry/axiom audit below, whether or not optional plugin scripts are available. Record the build and proof-audit outcomes separately; passing `lake build` does not establish completed proofs.
5. Stage or commit only if the user asked, and only the files touched in this session.

## Useful Prompts

- "Run a Lean checkpoint."
- "Verify this Lean work before we commit."
- "Check for remaining sorries and nonstandard axioms."


## Native proof audit (no plugin required)

1. State the audit scope: enumerate every named declaration being claimed as
   verified, including changed helper lemmas and definitions. Record files and
   qualified names; an audit of one theorem is not a whole-project audit.
2. Use `rg -n '\b(sorry|admit|axiom)\b' --glob '*.lean' <source-paths>`
   to locate candidate placeholders and assumptions. This is a source triage
   step: comments/strings may match, and macros or imported dependencies may
   introduce assumptions without matching source text. Do not infer proof
   completeness from an empty search.
3. In a temporary Lean file inside the project, import the affected modules and
   issue `#print axioms` for each scoped declaration. For example:

   ```lean
   import MyProject.Module
   #print axioms MyProject.targetTheorem
   #print axioms MyProject.helperLemma
   ```

   Run `lake env lean <audit-file>` using the project's pinned toolchain after
   its build. Retain the output and inspect every scoped declaration. Lean
   reports transitive axiom dependencies, including assumptions in imported
   proofs. A zero exit status from this command means the inspection executed;
   it does not mean the printed assumptions are acceptable.
4. Report every `sorryAx` dependency as an incomplete proof, including uses
   introduced by dependencies. Record custom axioms and any compiler/native
   evaluation trust (`Lean.trustCompiler` or version-specific `_native` axioms)
   as assumptions requiring the project's stated policy. The conventional
   logical axioms `propext`, `Classical.choice`, and `Quot.sound` may be allowed
   by that policy; do not silently expand its allowlist. List direct `axiom`
   declarations even when no audited theorem uses them.
5. A completed audit requires a recorded result for every declaration in scope,
   no remaining `sorryAx`, and disposition of every other assumption. Report
   compilation and audit separately, with unresolved findings blocking a
   claim of a completed proof. Preserve placeholders while reporting them; do
   not delete statements or weaken goals to obtain a clean build.

See [Lean's proof validation reference](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
for the native axiom-reporting contract. Optional plugin scripts can supplement
this procedure but are not required and must not replace scoped inspection.

### Reproducible successful-build/incomplete-proof example

The standalone pack includes `examples/proof-audit` beside this skill, pinned to Lean
4.34.1 with no dependencies or vendor scripts. From that directory:

```sh
lake build
lake env lean Audit.lean
```

`lake build` succeeds while warning that `AuditFixture.unfinished` uses
`sorry`. The audit reports `sorryAx` for both `unfinished` and
`dependsOnUnfinished`, even though the latter contains no placeholder. It
reports `AuditFixture.localAssumption` for the direct axiom and the theorem
that uses it, while `AuditFixture.proved` has no axiom dependencies. The build
is successful; the scoped proof audit fails completeness and records the
custom assumption. Run the pack's regression with
`python3 -m unittest discover -s tests -v`; it copies the fixture into an
isolated temporary project and checks these native Lean outputs.
