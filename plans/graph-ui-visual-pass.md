---
title: "Graph UI Visual Pass (fallback)"
status: draft
created: 2026-04-22
owner: jbl
---

# Graph UI Visual Pass

A net-new visual treatment for `wiki-graph-ui`, parked here as a fallback in case the Cosmograph swap (R15) doesn't land the desired feel.

This is **not a restoration** — no glow / halo / 3D treatment was ever in the original spec or any commit. This is a deliberate, additive design pass.

## Goals

1. Premium, dense-information feel — not generic "force-graph demo."
2. Strong cluster legibility at desktop and mobile.
3. Zero-build-step constraint preserved (static HTML/CSS/JS behind nginx).
4. Performance budget: 60 fps pan/zoom at 700 nodes on mid-tier mobile.

## Non-goals

- New layout algorithm (handled by R15 / Cosmograph swap).
- Changes to the API, node frontmatter, or wiki content model.

## Visual treatment

### Palette
- Keep golden-angle HSL per community (`hue = c * 137.508 % 360`).
- Drop saturation 65→58, raise lightness 58→62 — slightly desaturated for the dark BG so nodes don't vibrate on AMOLED screens.
- Background: existing `#0b0e14`. Edges: `rgba(124,140,168,0.18)` (currently 0.25 — too loud at high node count).

### Node rendering (3 layers, additive)
1. **Halo** — 2.4× radius radial gradient, `globalCompositeOperation: "lighter"`, alpha 0.95 → 0 falloff. Rendered from a per-color cached 64×64 offscreen sprite. Cluster glows enrich each other.
2. **Disc** — solid fill at exact community color, 0.6 px (screen-space) inset stroke `rgba(8,10,14,0.55)` to crisp the edge against the halo.
3. **Specular** — small white arc at upper-left, `r * 0.28` radius at `(-r * 0.32, -r * 0.32)`, alpha 0.55. Reads as 3D depth.

This is the same approach we tried in PR #20. The reason it "looked worse" there: it landed on top of the post-PR-#18 force layout regression, which scattered nodes into a circle. Halos on top of un-clustered nodes muddy. **Halos on top of tight Cosmograph clusters look premium** — the halos are doing the work of "this is one cluster" instead of fighting against it.

### Edges
- Tier-weighted opacity: tier-1 = 0.35, tier-2 = 0.22, tier-3 = 0.12.
- Highlight (path mode, selected node neighbors): `#5eead4` at 0.85, 1.5 px screen-space.
- Dim non-path during path/ask mode: 0.05.

### Labels
- Display only when zoom factor > 1.4 OR node is hovered/selected/path/ask-subgraph member.
- Font: `system-ui, -apple-system, "SF Pro Text"` 11 px screen-space, white, slight 1 px black halo via `ctx.strokeText` first.

### Side panel (mobile-first)
- Bottom sheet on mobile (height: 60vh, drag handle, dismiss-on-swipe-down).
- Right rail on desktop (≥ 768 px wide), 360 px wide.
- Tabs: Overview / Content / Neighbors.
- Markdown rendering for the wiki page body via the inline renderer from PR #18.
- This is the only feature from PR #18 worth restoring — the visual rendering parts of #18 are obsolete once Cosmograph lands.

## Phasing

If the Cosmograph swap lands and the user is not happy:
- Phase V1: Halo + disc + specular pass on top of Cosmograph (Cosmograph supports custom point shaders or we layer a transparent canvas over the Cosmograph WebGL canvas just for halo).
- Phase V2: Edge tier-weighted opacity + selected/dim edge palette.
- Phase V3: Mobile bottom sheet + tabs + markdown content panel.

If the Cosmograph swap does not land:
- Phase A1: Server-side precomputed layout (R15 option a). 1000+ FR iterations offline, write x/y to graph.json, client only does pan/zoom. Tight clusters without giving up the dependency-free image.
- Phase A2..V1..V2..V3 as above.

## Out of scope
- Animated transitions on filter changes (deferred).
- Node icons (deferred — the legend in the side panel is enough).
- Color-blind mode toggle (deferred — need user feedback first).

## References
- Original (never-shipped) glow code: `git show da26467 -- wiki-graph-ui/app.js`
- Cosmograph: https://cosmograph.app/docs-general/whats-new/
- Mobile bottom sheet pattern from PR #18: `git show 58059ff -- wiki-graph-ui/app.js wiki-graph-ui/styles.css wiki-graph-ui/index.html`
