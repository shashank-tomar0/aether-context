---
name: context7
description: Context engineering and state preservation protocol. Ensures session continuity, compressed architectural memory, structured handoffs between subagents, and zero knowledge loss across token window resets.
---

# Context7 Skill

## Directives
1. **Persistent Anchor**: Maintain `ai.md` at workspace root as the single source of truth for all architectural decisions, pending tasks, dependency graphs, and environment configurations.
2. **Deterministic Context Handoff**: Whenever a major milestone is reached or before switching focus between backend and frontend, update `ai.md` with:
   - Current commit/branch state
   - Active services and port mappings
   - Exact endpoints verified and contracts frozen
   - Unresolved bugs or edge cases
   - Next immediate 3 atomic actions
3. **Zero Hallucination Anchor**: If another agent or fresh instance picks up the workspace, reading `ai.md` must be sufficient to achieve instant full situational awareness in under 30 seconds without reading hundreds of raw logs.
