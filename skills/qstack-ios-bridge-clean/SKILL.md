---
name: qstack-ios-bridge-clean
description: "Remove an iOS debug bridge and verify the release build has no bridge residue."
---

# iOS Bridge Clean

## Requirements

- Target iOS source and Swift or Xcode release-build capability.

## Procedure

1. Inventory the debug package or target, compile-condition imports, boot hooks, generated accessors, and marker annotations. Identify application state owned by the user.
2. Remove bridge-owned package references, debug startup code and generated artifacts within the requested scope. Preserve hand-written application logic.
3. Search for lingering references, build the release configuration, and inspect available binary symbols for bridge residue. Report files removed and rollback information.

## Upstream sources

- Inventory DebugBridge wiring, remove bridge-owned pieces, and verify a release build. [gstack/ios-clean](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ios-clean/SKILL.md#L135)
