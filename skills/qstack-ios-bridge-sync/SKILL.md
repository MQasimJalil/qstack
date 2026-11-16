---
name: qstack-ios-bridge-sync
description: "Regenerate a SwiftUI debug bridge after state or bridge changes."
---

# iOS Bridge Sync

## Requirements

- Existing iOS debug bridge, its generator and Swift build tools. Device checks require a physical device.

## Procedure

1. Locate the installed Debug target, generated accessors, canonical state models and project generator. Record the intended schema change.
2. Regenerate owned artifacts using the maintained tool. Inspect the diff and keep hand-written logic outside regeneration.
3. Build the Debug app, launch on the intended device and confirm the expected accessor schema hash and exposed state. Report generated files and build and device evidence.

## Upstream sources

- Refresh generated state accessors and verify the new schema on a live device. [gstack/ios-sync](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ios-sync/SKILL.md#L100)
