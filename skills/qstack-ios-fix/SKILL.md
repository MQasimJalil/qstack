---
name: qstack-ios-fix
description: "Fix a reproducible iOS defect with before-and-after evidence on a physical device."
---

# iOS Fix

## Requirements

- A physical iOS device, build tools, and a project-supported UI or debug adapter.

## Procedure

1. Reproduce the exact flow on the affected build. Capture the wrong result and a reproducible app-state snapshot if the adapter supports it.
2. Trace the failure through SwiftUI state, the view model and underlying mutation. Apply the smallest change that corrects the demonstrated cause.
3. Rebuild and launch on the intended device. Restore the snapshot or replay the inputs and compare the visible result. Add a regression fixture when the project supports it and coverage is missing.
4. Report the exact baseline and patched builds, relevant source, replay result, and any device-only gap.

## Upstream sources

- Capture the bug state, trace the actual Swift cause, and replay the same state after fixing. [gstack/ios-fix](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ios-fix/SKILL.md#L102)
