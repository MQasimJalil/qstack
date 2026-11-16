---
name: qstack-catch-up
description: "Catch the user up on changes since their last message and present the decisions that still need them, in text or a subtitled video."
---

# Catch Up

## Procedure

1. Use the user’s last message as the start, and gather verified changes, relevant current run or PR states, and still-open decisions. Stay read-only apart from producing requested media.
2. Keep the text catch-up short. Use a compact visual for a connected change when it helps, and mark completed, running, failed, or unchecked outcomes using the real evidence.
3. For each decision only the user can make, state the call, available options or your recommendation, evidence, and downside. Include any required action and link that enables it.
4. For requested video, storyboard only meaningful changes from available captures, diagrams, or verified data. Render a silent landscape video with legible burned-in subtitles and enough time to read each slide.
5. Inspect a frame from each slide at the intended viewing size and check subtitle duration. Deliver the video with the same decision list and report any render limitation.

## Upstream sources

- Read-only account of meaningful changes and decisions still waiting for the user. [pstack/ketchup](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/ketchup/SKILL.md#L13)
- Silent subtitled visual walkthrough built from verified evidence, with the same decision handoff. [pstack/ketchup-video](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/ketchup-video/SKILL.md#L11)
