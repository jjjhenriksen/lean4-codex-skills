# Lean 4 Codex Skills 🦀

[![Codex](https://img.shields.io/badge/Codex-v2-4B0082?style=flat-square)](https://github.com/openclaw/codex)
[![Lean 4](https://img.shields.io/badge/Lean_4-latest-FF6F00?style=flat-square)](https://lean-lang.org)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

**Codex skill pack for Lean 4 formalization workflows.** Teach your coding agent to write Lean — from drafting theorem statements and filling sorries, to diagnosing toolchain issues and reviewing proofs.

This is the tooling side of an ongoing research interest in **LLM-assisted theorem proving and autoformalization** — using language models not as proof checkers, but as collaborative formalization partners guided by structured skill definitions.

---

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

Each skill is intentionally **thin and focused** — designed to point Codex toward the right workflow without loading a monolithic instruction file every time.

---

## Install

```bash
cp -R skills/lean4-* ~/.codex/skills/
```

Start a new Codex session so the skills are discovered, or run:

```bash
codexctl skills rescan
```

---

## Recommended Workspace Setup

For best results, use these skills in a Lean workspace with:

- `lean-toolchain`
- `lakefile.lean` or `lakefile.toml`
- Working `lean` and `lake` commands (usually via `elan`)

### Optional: Vendor Plugin

If your workspace also contains Cameron Freer's `lean4-skills` workflow pack:

```
vendor/lean4-plugin/
```

...set an env file so the skills can reference it:

```bash
export LEAN4_PLUGIN_ROOT="$PWD/vendor/lean4-plugin"
export LEAN4_SCRIPTS="$LEAN4_PLUGIN_ROOT/lib/scripts"
export LEAN4_PYTHON_BIN="${LEAN4_PYTHON_BIN:-python3}"
```

Then source it before starting your Codex session:

```bash
source ./lean4-codex.env 2>/dev/null || true
```

---

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

---

## Why This Exists

Lean 4 is a powerful proof assistant with a steep learning curve. These skills lower that curve by giving Codex agents structured, role-specific knowledge about Lean workflows — so the agent can mentor, formalize, prove, review, and diagnose without needing the full Lean pedagogy baked into every conversation.

This is particularly useful for **autoformalization research**: iterating on how LLMs translate informal mathematical claims into machine-checkable Lean statements, with structured skill definitions that evolve as we learn what works.

---

## Notes

These skills were adapted from two sources:

- Pavel's Lean mentor orientation prompt
- Cameron Freer's `lean4-skills` workflow structure

They do not vendor the full upstream Lean workflow pack. If you want the scripts and full command references, add that repository separately under your Lean workspace.

---

## Related

- [jjjhenriksen/Artemis-Lost](https://github.com/jjjhenriksen/Artemis-Lost) — AI-assisted narrative game, another angle on LLM-guided interaction
- [jjjhenriksen/HCI-Chapman-Connect](https://github.com/jjjhenriksen/HCI-Chapman-Connect) — HCI prototype exploring legible system design
