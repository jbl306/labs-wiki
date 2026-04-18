---
title: "Mobile-First Graph UI Design for Wiki Systems"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "18966277cc2d851def0d3ab62f0f8bc086251d5a0cc524d2697ef2d9766a9892"
sources:
  - raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
quality_score: 100
concepts:
  - mobile-first-graph-ui-design-for-wiki-systems
related:
  - "[[AXI Design Principles for Agent-Ergonomic CLI Tools]]"
  - "[[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]]"
tier: hot
tags: [graph-ui, mobile, responsive-design, accessibility, wiki]
---

# Mobile-First Graph UI Design for Wiki Systems

## Overview

Mobile-first graph UI design adapts complex, node-based visualizations for touch devices, ensuring usability and accessibility. This approach is crucial for knowledge graph interfaces, which often rely on dense, interactive layouts that must be navigable on small screens.

## How It Works

Mobile-first graph UI design begins by prioritizing the needs of touch-based devices, such as smartphones and tablets. The design process starts with the implementation of responsive layouts, typically using CSS media queries to adapt elements for screens ≤900px wide. Key interface components, such as drawers and sidebars, are reimagined as sliding panels that can be toggled via touch controls (e.g., hamburger menus).

Accessibility is enhanced by increasing input sizes to 16px, preventing unwanted zoom on iOS devices, and ensuring touch targets are at least 44px, which aligns with accessibility guidelines for finger navigation. Safe-area insets are used to avoid UI elements being obscured by device notches or rounded corners, and dvh (dynamic viewport height) units ensure layouts adapt to browser chrome changes (e.g., when the keyboard appears).

Pointer Events replace mouse-only handlers, allowing for unified gesture detection across devices. This includes pinch-to-zoom (tracking active pointers), tap-vs-drag detection (using slop thresholds and timing), and expanded hit-radius for coarse pointers (e.g., stylus or finger). Event listeners for visualViewport and orientationchange ensure the UI responds dynamically to device rotations and viewport resizing.

The UI is served as a zero-build static site via nginx, with runtime configuration swapping API endpoints for LAN/WAN compatibility. Progressive Web App (PWA) meta tags and theme-color settings improve integration with mobile OS features, such as home screen shortcuts and status bar coloring.

Testing involves rebuilding the container and verifying HTTP responses, UI element presence, and interaction fidelity. The design is validated by direct user interaction and audit logging in the wiki system.

## Key Properties

- **Responsive Layout:** Adapts to screen sizes ≤900px, using sliding drawers and touch-friendly controls.
- **Accessibility:** 16px input fields, 44px touch targets, safe-area insets, dvh units for dynamic viewport adaptation.
- **Unified Pointer Events:** Supports pinch-to-zoom, tap-vs-drag, and expanded hit-radius for coarse pointers.
- **PWA Integration:** Theme-color and meta tags for mobile OS compatibility and home screen integration.

## Limitations

Mobile-first design can lead to reduced information density compared to desktop layouts, potentially requiring additional navigation steps. Some advanced graph interactions (e.g., multi-node selection, complex filtering) may be harder to implement or less intuitive on touch devices. Compatibility issues can arise with older browsers or devices lacking full Pointer Events support.

## Example

The session implemented a sliding drawer sidebar, hamburger menu, and pinch-to-zoom gesture handling for the wiki graph UI at http://graph.jbl-lab.com. CSS was rewritten for mobile-first responsiveness, and JavaScript handlers were updated to use Pointer Events for unified touch and mouse support.

## Visual

No explicit diagrams included, but the text describes UI elements such as sliding drawers, hamburger menus, and touch targets.

## Relationship to Other Concepts

- **[[AXI Design Principles for Agent-Ergonomic CLI Tools]]** — Both focus on interface ergonomics, but AXI is CLI-focused while this is graphical/mobile.

## Practical Applications

Mobile-first graph UIs are essential for knowledge management systems accessed on the go, such as personal wikis, collaborative research platforms, and agent dashboards. They enable users to explore complex relationships and communities in knowledge graphs without being tethered to desktop environments.

## Sources

- [[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]] — primary source for this concept
