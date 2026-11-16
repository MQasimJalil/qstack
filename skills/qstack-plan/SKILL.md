---
name: qstack-plan
description: Turn a proposed change into one engineering plan with explicit ownership, a reachable failure, and appropriate checks.
---

# Plan

Trace the normal entry point and identify the state or data owner. State the user-visible behavior and one realistic way the implementation could violate it. Check how a failure propagates across the relevant boundary and identify the assumption the design depends on.

When the change creates or moves a boundary, sketch two materially different ownership or interface shapes. Choose the smaller interface that keeps the invariant in one place. Record an actual tradeoff and reuse the existing entry point where it supports the contract.

Use signatures, state ownership, and failure paths to expose differences between the shapes. Screen for pass-through APIs, policy copied across modules, callers reaching into implementation details, and hand-synced lists. For authorized implementation, keep the agreed contract visible and reopen the design if several changes require exceptions to it.

Turn the most consequential failure into an observable assertion. Select a bounded model check for meaningful ordering risk, a browser property for a browser-visible contract, and existing project checks for the code they cover. Give each selected check its distinct job and the evidence it must produce. Carry that plan into modeling, review, and verification.
