---
name: qstack-design-motion
description: "Animate an approved design for an accessible web page or a seamless showcase loop."
---

# Design Motion

## Requirements

- Use a browser or timeline renderer for deterministic frames and a video encoder for MP4 or GIF deliverables.

## Procedure

1. Identify whether the deliverable is website motion or a showcase. Anchor the work to the approved frame, the visual story, and the requested size and format.
2. Rebuild and compare the static frame before animation. For a website, animate the section where motion explains something and verify that reduced motion and disabled scripts leave content visible.
3. For a showcase, use a controllable clock and explicit state reset. Keep the approved composition at rest and capture the candidate loop at a fixed frame rate.
4. Check that a frame repeats at the loop boundary, that the reset reaches the initial empty beat, that the rest frame matches the still, and that motion stays within the intended bounds. Inspect a contact sheet before final encoding.
5. Export the requested artifacts. The showcase defaults are an H.264 MP4, a loop GIF, and an 800 by 500 GIF. Record dimensions, duration, frame rate, and any approved departure from the still.

## Upstream sources

- Approved-frame fidelity, restrained website motion, and deterministic showcase capture [gstack/design-motion](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/design-motion/SKILL.md#L124)
