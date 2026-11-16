# Agent capabilities

Choose an installed skill by the outcome it owns. Its procedure describes the actions and acceptance evidence. Use the host's equivalent capabilities at each step.

| Capability | Portable execution |
| --- | --- |
| Read, search, and edit project files | Use the agent's workspace tools or the system shell. Resolve paths from the selected project. Use a diff when a procedure depends on the exact change. |
| Run a project check | Use the number and scope of checks selected in the plan. Capture the command, revision, result, and relevant output. A missing runtime is incomplete evidence. |
| Run an independent reviewer or parallel worker | Use independent contexts when the user authorized delegation and the host provides it. Supply the same frozen scope to reviewers. On a single-agent host, run the applicable checks sequentially and report the actual coverage. |
| Drive an app, browser, or device | Use an available browser, CLI, or device driver. Start an isolated instance when the workflow changes data. Record the real interaction and the resulting state. |
| Work with deployment, CI, or external services | Use the project's configured provider and credentials. Follow the user's authorization for publication, merges, deployments, installations, or spending. Hosted and device-specific procedures declare the dependencies they still need. |
| Persist a decision or hand off work | Use Markdown, JSON, TSV, or the host's equivalent. Keep a source path or artifact for each claimed result. |

The executable pilot supports Codex and Claude Code, a custom stdio driver via `--agent-command`, or a chat-agent file bridge. Any agent that can read Markdown can use `qstack skill <name>`, even if its host does not discover installed skills automatically. The bundled pilot includes TLC and Bombadil integration. The other procedures use the tools and project setup named in their requirements.

When an upstream alias selects a mode, its export includes that choice. For example, `qstack skill gstack:qa-only` activates report mode, and `qstack skill gstack:unfreeze` selects release of a session boundary. Canonical skills also accept the user's explicit mode request.

The upstream notices are in [gstack's MIT license](licenses/gstack.txt) and [pstack's MIT license](licenses/pstack.txt). [The catalog](catalog.md) links to the pinned source for each adaptation.
