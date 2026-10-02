# Lean 4 Codex Skills 🦀

[![Codex](https://img.shields.io/badge/Codex-v2-4B0082?style=flat-square)](https://github.com/openclaw/codex)
[![Lean 4](https://img.shields.io/badge/Lean_4-latest-FF6F00?style=flat-square)](https://lean-lang.org)

**Codex skill pack for Lean 4 formalization workflows.** Teach your coding agent to write Lean — from drafting theorem statements and filling sorries, to diagnosing toolchain issues and reviewing proofs.

This is the tooling side of an ongoing research interest in **LLM-assisted theorem proving and autoformalization** — using language models not as proof checkers, but as collaborative formalization partners guided by structured skill definitions.


## Skills

| Skill | Purpose |
|-------|---------|
| [`lean4-mentor`](skills/lean4-mentor) | Front-door orientation — learn Lean as an interactive semantic environment |
| [`lean4-learn`](skills/lean4-learn) | Teaching, repo exploration, and mathlib navigation |
| [`lean4-formalize`](skills/lean4-formalize) | Draft and autoformalize — turn informal math into Lean declarations |
| [`lean4-prove`](skills/lean4-prove) | Fill sorries, prove existing declarations, proof repair |
| [`lean4-review`](skills/lean4-review) | Review, refactor, and proof golfing |
| [`lean4-checkpoint`](skills/lean4-checkpoint) | Build-checked save points, sorry/axiom audits, safe staging |
| [`lean4-doctor`](skills/lean4-doctor) | Diagnose toolchain issues — Lean, Lake, Mathlib, elan, imports |

`lean4-checkpoint` includes a plugin-independent native axiom audit and an
intentionally incomplete Lean example in its `examples/proof-audit` directory.
A successful build is reported separately from proof completeness. From this
checkout, `python3 -m unittest discover -s tests -v` builds the isolated example
and checks direct/transitive `sorryAx` and custom-axiom reports.

Each skill is intentionally **thin and focused** — designed to point Codex toward the right workflow without loading a monolithic instruction file every time.


## Install

```bash
cp -R skills/lean4-* ~/.codex/skills/
```

Start a new Codex session so the skills are discovered, or run:

```bash
codexctl skills rescan
```


## Recommended Workspace Setup

For best results, use these skills in a Lean workspace with:

- `lean-toolchain`
- `lakefile.lean` or `lakefile.toml`
- Working `lean` and `lake` commands (usually via `elan`)

### Optional: Pin the upstream workflow pack

The standalone skill installation above remains supported without upstream
code. Native Lean/Lake workflows and the bundled doctor/checkpoint examples
work independently; missing optional references are reported and skipped.

The authoritative upstream is [Cameron Freer's lean4-skills](https://github.com/cameronfreer/lean4-skills).
The command/guide/script layout has been verified at
[`b6243b85b9b0a0ddff5bb6773889044daf687f8e`](https://github.com/cameronfreer/lean4-skills/tree/b6243b85b9b0a0ddff5bb6773889044daf687f8e/plugins/lean4).
`optional-upstream.json` records that revision and the `plugins/lean4` plugin
subdirectory. This is a file-layout compatibility check; it does not certify
upstream proof automation or install/trust its host hooks.

From a Lean workspace, acquire it into a new destination (preserve any existing
checkout rather than replacing it):

```bash
git clone --no-checkout https://github.com/cameronfreer/lean4-skills.git vendor/lean4-skills
git -C vendor/lean4-skills checkout --detach b6243b85b9b0a0ddff5bb6773889044daf687f8e
git -C vendor/lean4-skills rev-parse HEAD
export LEAN4_PLUGIN_ROOT="$PWD/vendor/lean4-skills/plugins/lean4"
export LEAN4_SCRIPTS="$LEAN4_PLUGIN_ROOT/lib/scripts"
export LEAN4_PYTHON_BIN="${LEAN4_PYTHON_BIN:-python3}"
```

The checkout root is not the plugin root. Commands live under
`$LEAN4_PLUGIN_ROOT/commands`, the canonical skill/references under
`$LEAN4_PLUGIN_ROOT/skills/lean4`, and helpers under `$LEAN4_SCRIPTS`.
At this revision the upstream diagnostic guide is `commands/diagnose.md`;
the Codex split skill remains named `lean4-doctor` and points to that guide.

From this skill-pack checkout, verify an acquired plugin (use its absolute path
if the Lean workspace is elsewhere):

```bash
python3 scripts/check_optional_plugin.py \
  --root "$LEAN4_PLUGIN_ROOT" --require-compatible --require-pinned
```

The checker reads all guide/reference paths requested by the seven skills and
representative helper files, verifies the selected checkout revision/cleanliness,
and prints JSON. It does not run helper code. A missing default plugin is
`absent_optional` with exit zero; explicit `--require-compatible` fails on
missing files, and `--require-pinned` also fails for an unknown/different revision
or dirty checkout. Keep that evidence separate from Lean build/proof results.
CI fetches the recorded revision into an isolated checkout and repeats the
layout check, so changed references must stay compatible with the tested pin.

Save the exports in a workspace `lean4-codex.env` if desired. Every split skill
loads an existing env file before applying defaults. Without an explicit root,
`LEAN4_PLUGIN_ROOT` defaults to `$PWD/vendor/lean4-plugin`, preserving earlier
workspace layouts; `LEAN4_SCRIPTS` defaults to its `lib/scripts` directory.
Explicit script-root overrides remain respected, and quoted root paths may
contain spaces. To try a newer upstream version, verify its layout and native
workflows in a separate checkout before updating the recorded pin.


## Example Prompts

```
Use lean4-mentor to explain the difference between `simp` and `omega`.
```

```
Use lean4-learn to walk me through the mathlib docs for `Algebra/GroupPower`.
```

```
Use lean4-formalize to turn this informal claim into a Lean theorem statement:
  "The sum of the first n natural numbers is n(n+1)/2"
```

```
Use lean4-prove to fill the sorry in MergeSort.lean without changing the theorem statement.
```

```
Use lean4-review on this file and lead with correctness risks.
```

```
Run lean4-doctor and diagnose why Lake is failing to resolve mathlib imports.
```


## Why This Exists

Lean 4 is a powerful proof assistant with a steep learning curve. These skills lower that curve by giving Codex agents structured, role-specific knowledge about Lean workflows — so the agent can mentor, formalize, prove, review, and diagnose without needing the full Lean pedagogy baked into every conversation.

This is particularly useful for **autoformalization research**: iterating on how LLMs translate informal mathematical claims into machine-checkable Lean statements, with structured skill definitions that evolve as we learn what works.


## Notes

These skills were adapted from two sources:

- Pavel's Lean mentor orientation prompt
- Cameron Freer's `lean4-skills` workflow structure

They do not vendor the full upstream Lean workflow pack. If you want the scripts and full command references, add that repository separately under your Lean workspace.



## Licensing status

This repository currently publishes no project license file. The MIT badge
linked to a nonexistent `LICENSE` and has been removed. Adding a license
requires an explicit maintainer licensing decision and attribution review for
the adapted source material described above.
