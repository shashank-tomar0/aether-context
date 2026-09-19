---
name: taste-skill
description: Anti-slop frontend and UI design rules. Enforces typographic hierarchy, balanced spatial cadence, deliberate contrast, refined dark aesthetics, and Refero-level real-world polish instead of generic AI component templates.
---

# Taste Skill (Anti-Slop UI)

## Philosophy
Generic AI UI is easily spotted: flat purple gradients, identical cards with centered text, zero typographic rhythm, sterile Tailwind defaults, and generic illustrations. Taste is intentional constraint, variance, depth, and micro-delight.

## Design Rules
1. **Typography**:
   - Strict hierarchical scale (e.g., display 48-64px tracking tight, headline 28-36px, body 14-16px, mono meta 11-13px).
   - High-contrast headlines with muted, readable secondary copy (never low-contrast unreadable grey-on-black).
   - Distinctive typography pairings: clean grotesque/geometric sans (Inter, Geist Sans, Plus Jakarta Sans) paired with crisp monospace (Geist Mono, JetBrains Mono) for metrics/code.
2. **Color & Surface Architecture**:
   - Deep neutral palette: pure obsidian/charcoal foundations (`#09090b`, `#0f1117`, `#121212`) over generic dark blues.
   - Subtle 1px borders with fine opacity (`rgba(255,255,255,0.08)` to `0.12`) defining structural boundaries.
   - Purposeful accent colors (e.g., emerald green for live states, electric cyan, or warm amber) used sparingly (max 5-10% surface area).
3. **Density & Spatial Rhythm**:
   - High data density where users need information; generous breathing room in hero and focal areas.
   - Consistent 4px/8px grid system.
4. **Real-world Refero Standards**:
   - Every interface state must be accounted for: loading skeletons, empty states, error fallbacks, active streams.
   - Real data tables, interactive graphs, and real-time feeds instead of static placeholder lorem ipsum.
