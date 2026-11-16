---
name: qstack-design-html
description: "Build production-quality HTML or a framework component from an approved design."
---

# Design Html

## Requirements

- Use a browser to verify the rendered page. Pretext is needed for the layout operations that use it.

## Procedure

1. Load the approved mockup, design specification, and tokens where available. Identify the content structure and states that the implementation must reproduce.
2. Use the project's existing framework when delivering into an app. Choose the Pretext layout operation according to the content: resize-aware blocks, self-sizing cards, tightly fitted bubbles, or editorial line layout. Use the project layout primitive where it provides the same behavior.
3. Build semantic markup with reusable design tokens, keyboard controls, accessible names, and explicit loading, empty, and error states as needed. Preserve the approved visual hierarchy.
4. Render the result at narrow and wide widths. Check real text wraps, long content, tab order, focus, and visual fidelity. Run available lint and page checks and correct material findings.
5. Deliver the HTML or component with verification screenshots and any extracted tokens that should be shared.

## Upstream sources

- Content-aware Pretext routing, framework-native delivery, and verification at multiple viewport sizes [gstack/design-html](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/design-html/SKILL.md#L322)
