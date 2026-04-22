---
title: "Taste-Skill Design System for UI Consistency"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "8fde9c682fa2180a86ed53a5cd3c3e4eb8b2053c8c9f3aa44cb67b6ca8eba25c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
quality_score: 56
concepts:
  - taste-skill-design-system-ui-consistency
related:
  - "[[React Dashboard Redesign with TypeScript and Tailwind CSS]]"
  - "[[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]]"
tier: hot
tags: [design-system, ui, tailwindcss, theme, dark-mode]
---

# Taste-Skill Design System for UI Consistency

## Overview

The taste-skill design system is a set of design principles and reusable UI components guiding the visual language of the NBA ML Engine dashboard redesign. It ensures a consistent minimalist aesthetic with a warm monochrome color palette, Geist fonts, and a single emerald accent color, supporting industrial data density for analytics.

## How It Works

The design system is implemented as a collection of 7 taste-skill files installed globally (~/.agents/skills/) that define UI style rules, color tokens, typography, and component styling guidelines. These principles drive the React frontend's CSS custom properties, Tailwind CSS configuration, and component styling.

Key elements include:
- Minimalist-UI base style emphasizing clarity and simplicity
- Warm monochrome palette with light mode canvas color (#F7F6F3) and dark mode OLED black (#0A0A0A)
- Single emerald accent color (#059669 in light, #34D399 in dark) for highlights and interactive elements
- Geist fonts loaded from Google Fonts for a clean, modern typographic style
- Industrial data density approach to present many metrics and charts without clutter

The design tokens are defined in CSS custom properties within the Tailwind `@theme` directive, enabling seamless theme switching and consistent color usage across components. Dark mode is toggled by adding/removing a `.dark` class on the root element, with localStorage persistence for user preference.

Components such as SignalCard, DataTable, Badge, and charts are styled to conform to these design tokens, ensuring a unified look and feel. The NavBar uses floating pill navigation with a backdrop blur for modern UI aesthetics.

This system allows rapid UI development with consistent branding and usability while supporting complex data visualization needs.

## Key Properties

- **Design Tokens:** CSS custom properties defining colors, fonts, shadows, and accents for light and dark themes.
- **Font Family:** Geist and Geist Mono fonts loaded via Google Fonts CDN.
- **Color Palette:** Warm bone (#F7F6F3) for light canvas, OLED black (#0A0A0A) for dark, emerald accent (#059669/#34D399).
- **Theme Switching:** Dark mode toggled via `.dark` class with localStorage persistence.

## Limitations

The design system is tailored specifically for this dashboard's analytic use case and may not generalize to other UI domains without adaptation. The reliance on global taste-skill files requires coordination for updates. Dark mode styling requires thorough testing to avoid contrast or accessibility issues.

## Example

Tailwind CSS theme block example defining design tokens:

```css
@theme light {
  :root {
    --color-canvas: #F7F6F3;
    --color-accent: #059669;
    --font-sans: 'Geist', sans-serif;
  }
}

@theme dark {
  :root {
    --color-canvas: #0A0A0A;
    --color-accent: #34D399;
    --font-sans: 'Geist', sans-serif;
  }
}
```

Dark mode toggle React hook snippet:

```tsx
const [darkMode, setDarkMode] = useState(() => localStorage.getItem('darkMode') === 'true');

useEffect(() => {
  if (darkMode) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
  localStorage.setItem('darkMode', darkMode.toString());
}, [darkMode]);
```

## Relationship to Other Concepts

- **[[React Dashboard Redesign with TypeScript and Tailwind CSS]]** — Design system guides styling of React components

## Practical Applications

Ensures UI consistency and brand identity across complex analytic dashboards. Facilitates rapid development with reusable design tokens and theme support. Improves user experience with clear typography, color contrast, and visual hierarchy tailored for data-dense interfaces.

## Sources

- [[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]] — primary source for this concept
