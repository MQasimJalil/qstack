---
name: qstack-ios-qa
description: "Exercise and verify a SwiftUI app on an authorized physical iOS device."
---

# iOS QA

## Requirements

- Physical iOS device with a supported UI or debug adapter. Rebuilding requires suitable build tooling.

## Procedure

1. Identify the device, app source, build and requested journey. Verify the device connection and app identity through authorized Xcode UI automation or a debug adapter.
2. Scope observation, interaction and state changes to the verified device. If the established Debug target relies on generated accessors, prepare them from the relevant Swift state.
3. Drive the real path. Capture screenshots, accessibility or console evidence, and actual state changes. Confirm gestures or transitions through their observed effect.
4. Release the session. Report the exact build, successful checks and specific adapter limitations.

## Upstream sources

- Use capability-scoped device sessions, verified builds, real interactions, and cleanup. [gstack/ios-qa](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ios-qa/SKILL.md#L139)
