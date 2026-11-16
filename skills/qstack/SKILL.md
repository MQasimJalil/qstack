---
name: qstack
description: Run the qstack engineering workflow from a grounded plan through evidence-backed verification. Use for an end-to-end qstack run or the cancel-and-retry pilot.
---

# Qstack

Use `qstack skills [search]` to find the workflow that matches the request. Read it with `qstack skill <name>` or open its installed `SKILL.md`. The command also resolves upstream names such as `gstack:qa-only` and `pstack:statechart`. For a topic that fits a single skill, apply that procedure directly.

For an end-to-end engineering change, use the companion skills in order. Give each phase the artifacts from the preceding phase and carry forward the same behavior and risk.

1. **qstack-plan** grounds the behavior, chooses a design, and selects the checks.
2. **qstack-model** checks risky event ordering with TLC when the plan calls for it. Carry the witness into the implementation or browser check.
3. Build against the chosen design, or snapshot the existing implementation. Use the project's normal entry points.
4. **qstack-review** reviews the implementation and the strength of the selected checks once. Resolve material findings before claiming readiness.
5. **qstack-verify** runs the selected checks against the reviewed input and links the evidence. Reuse completed evidence for the same input.

For the bundled pilot, run `qstack run --agent codex`, `qstack run --agent claude`, or the command adapter described by `qstack run --help`. When using a chat agent with filesystem access, run `qstack run --agent bridge --out <new-directory>` in a background terminal. Supply the plan and review replies requested in that directory and follow the run through its final receipt. For a project-local installation, invoke `node .qstack/runtime/bin/qstack.cjs` in place of `qstack`.

For another project, apply the same phases to its own source, model, and runtime commands. Read a companion skill when its phase starts. Preserve undecided product choices and the scope of the user's request.
