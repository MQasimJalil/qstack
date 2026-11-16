---
name: qstack-model
description: Turn a concrete ordering or state-machine risk into a bounded TLC check and an implementation or UI witness.
---

# Model

Use the smallest state space that preserves the ordering hazard. Map model actions to real implementation transitions and give the invariant a name that explains the harm. Describe the bound and make quiescent states explicit.

Run one protected check. For a new or changed invariant, run a deliberately broken control with the same invariant and bound to show that it can fail. Record the checked configuration, outcome, and the named actions and states of the counterexample. Use the actual witness to drive a corresponding runtime check when the behavior is observable. A runtime-only observation such as refresh can follow the modeled steps.

For a statechart, label each edge with the modeled action and each node with the observable phase. Highlight initial, terminal, and violating states. If the model is too large to display clearly, show the shortest violation paths and give the full state count separately. For reusable proof authoring across verification tools, use qstack-create-formal-verification.

Treat a violation in the protected model as a finding. Trace whether the design or the model's mapping to the implementation needs correction.
