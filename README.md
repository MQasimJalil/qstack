# qstack

Qstack gives coding agents 109 skills for planning, implementation, review, and verification. It combines overlapping gstack and pstack workflows and preserves distinct procedures. A runnable cancel-and-retry example connects TLA+ model checking with browser verification.

## Install with npx

With Node.js 18 or newer, npm, and Git installed, run this from the root of the project you want to use qstack in. The command installs project-local skills and a qstack CLI.

```sh
npx --yes --package="git+https://github.com/MQasimJalil/qstack.git" qstack setup --host codex
```

Use `--host claude` for Claude Code, or choose `cursor`, `opencode`, `gemini`, or `all`. Other agents can use `--skills-dir <path>` or read the instructions printed by the installed CLI.

```sh
node .qstack/runtime/bin/qstack.cjs skills
node .qstack/runtime/bin/qstack.cjs skills verification
node .qstack/runtime/bin/qstack.cjs skill qstack
```

Rerun setup to update. If you edited a file installed by qstack, setup reports the conflict before writing. For reproducible installations, append `#<commit-sha>` to the Git URL. See [agent capabilities](docs/agent-capabilities.md) for host and tool requirements.

## Use qstack in your project

Open the project in your coding agent and give it a specific change or behavior to verify.

> Use the qstack skill to plan, implement, review, and verify [describe the change]. Run the project's applicable build, lint, type, unit, and integration checks. Model risky event ordering with TLC and replay a user-visible witness in the browser when applicable. Save the commands, results, and evidence.

The agent uses your project's entry points and test tooling. The planning, review, and verification skills carry forward the same acceptance criteria so each check serves a distinct purpose. Use the project-local skill command above when your agent needs the workflow instructions explicitly.

### Core skills

| Skill | When to use it |
| --- | --- |
| [`qstack`](skills/qstack/SKILL.md) | Run the workflow from planning through verification and carry the evidence forward. |
| [`qstack-plan`](skills/qstack-plan/SKILL.md) | Trace the real entry point, choose a design, and turn reachable failures into concrete checks. |
| [`qstack-model`](skills/qstack-model/SKILL.md) | Check a bounded TLA+ model for ordering hazards in retries, cancellation, concurrency, or other state transitions. Use a deliberately broken control to prove a new invariant can fail. |
| [`qstack-review`](skills/qstack-review/SKILL.md) | Review the exact implementation once against the agreed behavior and strength of the evidence. |
| [`qstack-verify`](skills/qstack-verify/SKILL.md) | Exercise the normal entry point, replay a model witness when applicable, and tie evidence to the tested input. |
| [`qstack-qa`](skills/qstack-qa/SKILL.md) | Test a real browser, API, CLI, or background workflow and verify authorized fixes. |
| [`qstack-test-audit`](skills/qstack-test-audit/SKILL.md) | Find redundant or weak tests while preserving coverage that catches distinct failures. |
| [`qstack-create-formal-verification`](skills/qstack-create-formal-verification/SKILL.md) | Create a reusable project skill for a high-cost correctness risk that warrants formal checks. |
| [`qstack-create-verification-skill`](skills/qstack-create-verification-skill/SKILL.md) | Capture how to start the real app, drive a workflow, and verify observable results on future changes. |

The [full skill catalog](docs/catalog.md) lists all 109 skills, upstream aliases, and source mappings. `skill` also resolves aliases such as `pstack:statechart` and `gstack:qa-only`.

## Run the cancel-and-retry pilot

The packaged `run` command exercises the bundled example. It requires Python 3.10 or newer, Java, Docker running Linux containers, and an authenticated agent for planning and review.

```sh
node .qstack/runtime/bin/qstack.cjs run --agent codex
```

Use `--agent claude` for Claude Code or see `run --help` for custom command and file bridge adapters. The `pilot` command runs the deterministic TLC and Bombadil checks without an agent. Use `--tlc-jar <path>` to reuse a local copy of the pinned jar. The same commands run from a source checkout with `node bin/qstack.cjs`.

The pilot verifies that a late failure from a cancelled attempt cannot overwrite a successful retry. TLC finds a counterexample in the faulty model and checks the protected model. Qstack turns the counterexample into browser actions. Bombadil replays those actions in Chromium against both variants and checks the visible status after refresh.

The run prints the path to its HTML report and saves the plan, review, TLC logs, `handoff.json`, and browser traces under `qstack-runs/`. Use `--out <new-directory>` to choose another location.

## Upstream projects and attribution

| Project | Contribution |
| --- | --- |
| [gstack](https://github.com/garrytan/gstack) | Product and engineering planning, design and code review, QA, and release workflows. |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | Architecture, statechart modeling, verification, and evidence-driven engineering practices. |
| [TLA+ Tools](https://github.com/tlaplus/tlaplus) | TLC checks the bounded TLA+ model and produces the counterexample used in the pilot. |
| [Bombadil](https://github.com/antithesishq/bombadil) | Property-based browser testing drives Chromium and captures the verification traces. |

See the [synthesis notes](docs/synthesis.md) for examples of how the workflows were combined, the [catalog](docs/catalog.md) for pinned source links, and the upstream MIT notices for [gstack](docs/licenses/gstack.txt) and [pstack](docs/licenses/pstack.txt).
