---
title: "https://github.com/midudev/autoskills"
type: url
captured: 2026-04-10T12:47:46.698486+00:00
source: android-share
url: "https://github.com/midudev/autoskills"
content_hash: "sha256:942ee5b045c1ae49c286230cf2545a8a376f819d8014422520cfa0b4c55deaa7"
tags: []
status: ingested
---

https://github.com/midudev/autoskills

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T00:27:46+00:00
- source_url: https://github.com/midudev/autoskills
- resolved_url: https://github.com/midudev/autoskills
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: midudev/autoskills
Description: One command. Your entire AI skill stack. Installed.
Stars: 3529
Language: TypeScript

## README

<div align="center">

<a href="https://autoskills.sh">
<img src="https://autoskills.sh/og.jpg" alt="autoskills" />
</a>

# autoskills

**One command. Your entire AI skill stack. Installed.**

[autoskills.sh](https://autoskills.sh)

</div>

Scans your project, detects your tech stack, and installs the best AI agent skills from [skills.sh](https://skills.sh) automatically.

```bash
npx autoskills
```

## How it works

1. Run `npx autoskills` in your project root
2. Your `package.json`, Gradle files, and config files are scanned to detect technologies
3. The best matching AI agent skills are installed via [skills.sh](https://skills.sh)
4. If Claude Code is targeted, a `CLAUDE.md` summary is generated from the installed markdown files in `.claude/skills`

That's it. No config needed.

## Claude Code summary

If `claude-code` is auto-detected or passed with `-a`, `autoskills` also writes a `CLAUDE.md` file in your project root with a quick summary of the markdown files installed for Claude Code.

## Options

```
-y, --yes       Skip confirmation prompt
--dry-run       Show what would be installed without installing
-h, --help      Show help message
```

## Supported Technologies

Built to work across modern frontend, backend, mobile, cloud, and media stacks.

- **Frameworks & UI:** React, Next.js, Vue, Nuxt, Svelte, Angular, Astro, Tailwind CSS, shadcn/ui, GSAP, Three.js
- **Languages & Runtimes:** TypeScript, Node.js, Go, Bun, Deno, Dart
- **Backend & APIs:** Express, Hono, NestJS, Spring Boot
- **Mobile & Desktop:** Expo, React Native, Flutter, SwiftUI, Android, Kotlin Multiplatform, Tauri, Electron
- **Data & Storage:** Supabase, Neon, Prisma, Drizzle ORM, Zod, React Hook Form
- **Auth & Billing:** Better Auth, Clerk, Stripe
- **Testing:** Vitest, Playwright
- **Cloud & Infrastructure:** Vercel, Vercel AI SDK, Cloudflare, Durable Objects, Cloudflare Agents, Cloudflare AI, AWS, Azure, Terraform
- **Tooling:** Turborepo, Vite, oxlint
- **Media & AI:** Remotion, ElevenLabs

## Requirements

Node.js >= 22

## License

[CC BY-NC 4.0](./LICENSE) — [midudev](https://midu.dev)


## File: .gitignore

```
# build output
dist/

# generated types
.astro/

# dependencies
node_modules/

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# environment variables
.env
.env.production

# macOS-specific files
.DS_Store

# jetbrains setting folder
.idea/

# generated AI agent skills
.agents/
.claude/
skills-lock.json

```


## File: AGENTS.md

```
# AGENTS

<!-- fendo:start -->

## Supply Chain Security

This project has been hardened against supply chain attacks using [fendo](https://github.com/midudev/fendo).

### Rules for AI assistants and contributors

- **Never use `^` or `~`** in dependency version specifiers. Always pin exact versions.
- **Always commit the lockfile** (`pnpm-lock.yaml`). Never delete it or add it to `.gitignore`.
- **Install scripts are disabled**. If a new dependency requires a build step, it must be explicitly approved.
- **New package versions must be at least 1 day old** before they can be installed (release age gating is enabled).
- When adding a dependency, verify it on [npmjs.com](https://www.npmjs.com) before installing.
- Prefer well-maintained packages with verified publishers and provenance.
- Run `pnpm install` with the lockfile present — never bypass it.
- Do not add git-based or tarball URL dependencies unless explicitly approved.
- **Do not run `npm update`**, `npx npm-check-updates`, or any blind upgrade command. Review each update individually.
- **Use deterministic installs**: prefer `pnpm install --frozen-lockfile` over `pnpm install` in CI and scripts.
<!-- fendo:end -->

## Testing

- Tests use Node.js built-in test runner (`node:test`) and `node:assert/strict`.
- **Always destructure** the specific assert functions you need instead of importing the default `assert` object. Use `ok(...)` instead of `assert.ok(...)`, `strictEqual(...)` instead of `assert.strictEqual(...)`, etc.

```js
// ✅ Correct
import { ok, strictEqual, deepStrictEqual } from "node:assert/strict";

ok(value);
strictEqual(a, b);

// ❌ Wrong
import assert from "node:assert/strict";

assert.ok(value);
assert.strictEqual(a, b);
```

- Use the shared helpers from `tests/helpers.mjs` (`useTmpDir`, `writePackageJson`, `writeJson`, `writeFile`, `addWorkspace`) to avoid duplicating filesystem setup logic in tests.

## Output helpers

- **Never use `console.log` or `process.stdout.write` directly** in the CLI package (`packages/autoskills`). Use the `log` and `write` helpers exported from `colors.mjs` instead.

```js
// ✅ Correct
import { log, write } from "./colors.mjs";

log("hello");
write("raw output\n");

// ❌ Wrong
console.log("hello");
process.stdout.write("raw output\n");
```

```


## File: CLAUDE.md

```
# CLAUDE.md

<!-- autoskills:start -->

Summary generated by `autoskills`. Check the full files inside `.claude/skills`.

## Accessibility (a11y)

Audit and improve web accessibility following WCAG 2.2 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible".

- `.claude/skills/accessibility/SKILL.md`
- `.claude/skills/accessibility/references/A11Y-PATTERNS.md`: Practical, copy-paste-ready patterns for common accessibility requirements. Each pattern is self-contained and linked from the main [SKILL.md](../SKILL.md).
- `.claude/skills/accessibility/references/WCAG.md`

## Astro Usage Guide

Skill for building with the Astro web framework. Helps create Astro components and pages, configure SSR adapters, set up content collections, deploy static sites, and manage project structure and CLI commands. Use when the user needs to work with Astro, mentions .astro files, asks about static si...

- `.claude/skills/astro/SKILL.md`

## Deploy to Vercel

Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".

- `.claude/skills/deploy-to-vercel/SKILL.md`

## Design Thinking

Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beaut...

- `.claude/skills/frontend-design/SKILL.md`

## Node.js Backend Patterns

Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integration, and API design best practices. Use when creating Node.js servers, REST APIs, GraphQL backends, or microservices architectures.

- `.claude/skills/nodejs-backend-patterns/SKILL.md`
- `.claude/skills/nodejs-backend-patterns/references/advanced-patterns.md`: Advanced patterns for dependency injection, database integration, authentication, caching, and API response formatting.

## Node.js Best Practices

Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying.

- `.claude/skills/nodejs-best-practices/SKILL.md`

## Oxlint — High-Performance JS/TS Linter

Run and configure oxlint — the high-performance JavaScript/TypeScript linter built on the Oxc compiler stack. Use this skill whenever working in a project that has oxlint installed (check for `oxlint` in package.json devDependencies or an `.oxlintrc.json` / `oxlint.config.ts` config file). This i...

- `.claude/skills/oxlint/SKILL.md`

## SEO optimization

Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "sitemap optimization", or "search engine optimization".

- `.claude/skills/seo/SKILL.md`

## Tailwind CSS Development Patterns

Provides comprehensive Tailwind CSS utility-first styling patterns including responsive design, layout utilities, flexbox, grid, spacing, typography, colors, and modern CSS best practices. Use when styling React/Vue/Svelte components, building responsive layouts, implementing design systems, or o...

- `.claude/skills/tailwind-css-patterns/SKILL.md`
- `.claude/skills/tailwind-css-patterns/references/accessibility.md`
- `.claude/skills/tailwind-css-patterns/references/animations.md`: Usage:
- `.claude/skills/tailwind-css-patterns/references/component-patterns.md`
- `.claude/skills/tailwind-css-patterns/references/configuration.md`: Use the `@theme` directive for CSS-based configuration:
- `.claude/skills/tailwind-css-patterns/references/layout-patterns.md`: Basic flex container:
- `.claude/skills/tailwind-css-patterns/references/performance.md`: Configure content sources for optimal purging:
- `.claude/skills/tailwind-css-patterns/references/reference.md`: Tailwind CSS is a utility-first CSS framework that generates styles by scanning HTML, JavaScript, and template files for class names. It provides a comprehensive design system through CSS utility classes, enabling rapid UI development without writing custom CSS. The framework operates at build-ti...
- `.claude/skills/tailwind-css-patterns/references/responsive-design.md`: Enable dark mode in tailwind.config.js:

## TypeScript Advanced Types

Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for building type-safe applications. Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety in TypeScript pr...

- `.claude/skills/typescript-advanced-types/SKILL.md`

<!-- autoskills:end -->

```


## File: CODE_OF_CONDUCT.md

```
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
- Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:

- The use of sexualized language or imagery, and sexual attention or
  advances of any kind
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or email
  address, without their explicit permission
- Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement.
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
[https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].

[homepage]: https://www.contributor-covenant.org
[v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html

```


## File: CONTRIBUTING.md

```
# Contributing to AutoSkills

First off, thank you for considering contributing to AutoSkills! It's people like you that make open source such a great community.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, please [open an issue](../../issues) on GitHub. It's the best way to get things started.

## 2. Fork & create a branch

If this is something you think you can fix, then [fork AutoSkills](../../fork) and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-new-feature
```

Or for a general fix:

```sh
git checkout -b fix/typo-in-readme
```

## 3. Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help on your PR if you get stuck.

## 4. Get the style right

Your patch should follow the same coding conventions and style as the rest of the project. Please ensure:

- Your code is properly linted and formatted before pushing.
- All new features and bug fixes include relevant tests.
- Existing tests pass locally before committing.

## 5. Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with the main repository:

```sh
git remote add upstream https://github.com/midudev/autoskills.git
git checkout main
git pull upstream main
```

Then update your feature branch from your local copy of main, and push it!

```sh
git checkout 325-add-new-feature
git rebase main
git push --set-upstream origin 325-add-new-feature
```

Finally, go to GitHub and create a Pull Request on the main repository.

## 6. Keeping your Pull Request updated

If an maintainer asks you to rebase, they're saying that a lot of code has changed, and that you need to update your branch to easily merge it into the main project.

Thank you for contributing!

```


## File: LICENSE

```
Creative Commons Attribution-NonCommercial 4.0 International

Copyright (c) 2025 midudev

https://creativecommons.org/licenses/by-nc/4.0/

You are free to:

  Share — copy and redistribute the material in any medium or format
  Adapt — remix, transform, and build upon the material

Under the following terms:

  Attribution — You must give appropriate credit, provide a link to
  the license, and indicate if changes were made. You may do so in
  any reasonable manner, but not in any way that suggests the licensor
  endorses you or your use.

  NonCommercial — You may not use the material for commercial purposes.

  No additional restrictions — You may not apply legal terms or
  technological measures that legally restrict others from doing
  anything the license permits.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

```


## File: package.json

```
{
  "name": "autoskills-sh",
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro",
    "og": "node scripts/generate-og.mjs",
    "lint": "oxlint",
    "lint:fix": "oxlint --fix",
    "fmt": "oxfmt --write .",
    "fmt:check": "oxfmt --check ."
  },
  "dependencies": {
    "@tailwindcss/vite": "4.2.2",
    "astro": "6.1.5",
    "geist": "1.7.0",
    "tailwindcss": "4.2.2"
  },
  "devDependencies": {
    "oxfmt": "0.44.0",
    "oxlint": "1.59.0"
  },
  "engines": {
    "node": ">=22.12.0"
  },
  "packageManager": "pnpm@10.33.0"
}

```


## File: pnpm-lock.yaml

```
lockfileVersion: '9.0'

settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

importers:

  .:
    dependencies:
      '@tailwindcss/vite':
        specifier: 4.2.2
        version: 4.2.2(vite@7.3.2(@types/node@25.5.0)(jiti@2.6.1)(lightningcss@1.32.0))
      astro:
        specifier: 6.1.5
        version: 6.1.5(@types/node@25.5.0)(jiti@2.6.1)(lightningcss@1.32.0)(rollup@4.60.1)
      geist:
        specifier: 1.7.0
        version: 1.7.0(next@16.2.1(react-dom@19.2.4(react@19.2.4))(react@19.2.4))
      tailwindcss:
        specifier: 4.2.2
        version: 4.2.2
    devDependencies:
      oxfmt:
        specifier: 0.44.0
        version: 0.44.0
      oxlint:
        specifier: 1.59.0
        version: 1.59.0

packages:

  '@astrojs/compiler@3.0.1':
    resolution: {integrity: sha512-z97oYbdebO5aoWzuJ/8q5hLK232+17KcLZ7cJ8BCWk6+qNzVxn/gftC0KzMBUTD8WAaBkPpNSQK6PXLnNrZ0CA==}

  '@astrojs/internal-helpers@0.8.0':
    resolution: {integrity: sha512-J56GrhEiV+4dmrGLPNOl2pZjpHXAndWVyiVDYGDuw6MWKpBSEMLdFxHzeM/6sqaknw9M+HFfHZAcvi3OfT3D/w==}

  '@astrojs/markdown-remark@7.1.0':
    resolution: {integrity: sha512-P+HnCsu2js3BoTc8kFmu+E9gOcFeMdPris75g+Zl4sY8+bBRbSQV6xzcBDbZ27eE7yBGEGQoqjpChx+KJYIPYQ==}

  '@astrojs/prism@4.0.1':
    resolution: {integrity: sha512-nksZQVjlferuWzhPsBpQ1JE5XuKAf1id1/9Hj4a9KG4+ofrlzxUUwX4YGQF/SuDiuiGKEnzopGOt38F3AnVWsQ==}
    engines: {node: '>=22.12.0'}

  '@astrojs/telemetry@3.3.0':
    resolution: {integrity: sha512-UFBgfeldP06qu6khs/yY+q1cDAaArM2/7AEIqQ9Cuvf7B1hNLq0xDrZkct+QoIGyjq56y8IaE2I3CTvG99mlhQ==}
    engines: {node: 18.20.8 || ^20.3.0 || >=22.0.0}

  '@babel/helper-string-parser@7.27.1':
    resolution: {integrity: sha512-qMlSxKbpRlAridDExk92nSobyDdpPijUq2DW6oDnUqd0iOGxmQjyqhMIihI9+zv4LPyZdRje2cavWPbCbWm3eA==}
    engines: {node: '>=6.9.0'}

  '@babel/helper-validator-identifier@7.28.5':
    resolution: {integrity: sha512-qSs4ifwzKJSV39ucNjsvc6WVHs6b7S03sOh2OcHF9UHfVPqWWALUsNUVzhSBiItjRZoLHx7nIarVjqKVusUZ1Q==}
    engines: {node: '>=6.9.0'}

  '@babel/parser@7.29.2':
    resolution: {integrity: sha512-4GgRzy/+fsBa72/RZVJmGKPmZu9Byn8o4MoLpmNe1m8ZfYnz5emHLQz3U4gLud6Zwl0RZIcgiLD7Uq7ySFuDLA==}
    engines: {node: '>=6.0.0'}
    hasBin: true

  '@babel/types@7.29.0':
    resolution: {integrity: sha512-LwdZHpScM4Qz8Xw2iKSzS+cfglZzJGvofQICy7W7v4caru4EaAmyUuO6BGrbyQ2mYV11W0U8j5mBhd14dd3B0A==}
    engines: {node: '>=6.9.0'}

  '@capsizecss/unpack@4.0.0':
    resolution: {integrity: sha512-VERIM64vtTP1C4mxQ5thVT9fK0apjPFobqybMtA1UdUujWka24ERHbRHFGmpbbhp73MhV+KSsHQH9C6uOTdEQA==}
    engines: {node: '>=18'}

  '@clack/core@1.2.0':
    resolution: {integrity: sha512-qfxof/3T3t9DPU/Rj3OmcFyZInceqj/NVtO9rwIuJqCUgh32gwPjpFQQp/ben07qKlhpwq7GzfWpST4qdJ5Drg==}

  '@clack/prompts@1.2.0':
    resolution: {integrity: sha512-4jmztR9fMqPMjz6H/UZXj0zEmE43ha1euENwkckKKel4XpSfokExPo5AiVStdHSAlHekz4d0CA/r45Ok1E4D3w==}

  '@emnapi/runtime@1.9.2':
    resolution: {integrity: sha512-3U4+MIWHImeyu1wnmVygh5WlgfYDtyf0k8AbLhMFxOipihf6nrWC4syIm/SwEeec0mNSafiiNnMJwbza/Is6Lw==}

  '@esbuild/aix-ppc64@0.27.7':
    resolution: {integrity: sha512-EKX3Qwmhz1eMdEJokhALr0YiD0lhQNwDqkPYyPhiSwKrh7/4KRjQc04sZ8db+5DVVnZ1LmbNDI1uAMPEUBnQPg==}
    engines: {node: '>=18'}
    cpu: [ppc64]
    os: [aix]

  '@esbuild/android-arm64@0.27.7':
    resolution: {integrity: sha512-62dPZHpIXzvChfvfLJow3q5dDtiNMkwiRzPylSCfriLvZeq0a1bWChrGx/BbUbPwOrsWKMn8idSllklzBy+dgQ==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [android]

  '@esbuild/android-arm@0.27.7':
    resolution: {integrity: sha512-jbPXvB4Yj2yBV7HUfE2KHe4GJX51QplCN1pGbYjvsyCZbQmies29EoJbkEc+vYuU5o45AfQn37vZlyXy4YJ8RQ==}
    engines: {node: '>=18'}
    cpu: [arm]
    os: [android]

  '@esbuild/android-x64@0.27.7':
    resolution: {integrity: sha512-x5VpMODneVDb70PYV2VQOmIUUiBtY3D3mPBG8NxVk5CogneYhkR7MmM3yR/uMdITLrC1ml/NV1rj4bMJuy9MCg==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [android]

  '@esbuild/darwin-arm64@0.27.7':
    resolution: {integrity: sha512-5lckdqeuBPlKUwvoCXIgI2D9/ABmPq3Rdp7IfL70393YgaASt7tbju3Ac+ePVi3KDH6N2RqePfHnXkaDtY9fkw==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [darwin]

  '@esbuild/darwin-x64@0.27.7':
    resolution: {integrity: sha512-rYnXrKcXuT7Z+WL5K980jVFdvVKhCHhUwid+dDYQpH+qu+TefcomiMAJpIiC2EM3Rjtq0sO3StMV/+3w3MyyqQ==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [darwin]

  '@esbuild/freebsd-arm64@0.27.7':
    resolution: {integrity: sha512-B48PqeCsEgOtzME2GbNM2roU29AMTuOIN91dsMO30t+Ydis3z/3Ngoj5hhnsOSSwNzS+6JppqWsuhTp6E82l2w==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [freebsd]

  '@esbuild/freebsd-x64@0.27.7':
    resolution: {integrity: sha512-jOBDK5XEjA4m5IJK3bpAQF9/Lelu/Z9ZcdhTRLf4cajlB+8VEhFFRjWgfy3M1O4rO2GQ/b2dLwCUGpiF/eATNQ==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [freebsd]

  '@esbuild/linux-arm64@0.27.7':
    resolution: {integrity: sha512-RZPHBoxXuNnPQO9rvjh5jdkRmVizktkT7TCDkDmQ0W2SwHInKCAV95GRuvdSvA7w4VMwfCjUiPwDi0ZO6Nfe9A==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [linux]

  '@esbuild/linux-arm@0.27.7':
    resolution: {integrity: sha512-RkT/YXYBTSULo3+af8Ib0ykH8u2MBh57o7q/DAs3lTJlyVQkgQvlrPTnjIzzRPQyavxtPtfg0EopvDyIt0j1rA==}
    engines: {node: '>=18'}
    cpu: [arm]
    os: [linux]

  '@esbuild/linux-ia32@0.27.7':
    resolution: {integrity: sha512-GA48aKNkyQDbd3KtkplYWT102C5sn/EZTY4XROkxONgruHPU72l+gW+FfF8tf2cFjeHaRbWpOYa/uRBz/Xq1Pg==}
    engines: {node: '>=18'}
    cpu: [ia32]
    os: [linux]

  '@esbuild/linux-loong64@0.27.7':
    resolution: {integrity: sha512-a4POruNM2oWsD4WKvBSEKGIiWQF8fZOAsycHOt6JBpZ+JN2n2JH9WAv56SOyu9X5IqAjqSIPTaJkqN8F7XOQ5Q==}
    engines: {node: '>=18'}
    cpu: [loong64]
    os: [linux]

  '@esbuild/linux-mips64el@0.27.7':
    resolution: {integrity: sha512-KabT5I6StirGfIz0FMgl1I+R1H73Gp0ofL9A3nG3i/cYFJzKHhouBV5VWK1CSgKvVaG4q1RNpCTR2LuTVB3fIw==}
    engines: {node: '>=18'}
    cpu: [mips64el]
    os: [linux]

  '@esbuild/linux-ppc64@0.27.7':
    resolution: {integrity: sha512-gRsL4x6wsGHGRqhtI+ifpN/vpOFTQtnbsupUF5R5YTAg+y/lKelYR1hXbnBdzDjGbMYjVJLJTd2OFmMewAgwlQ==}
    engines: {node: '>=18'}
    cpu: [ppc64]
    os: [linux]

  '@esbuild/linux-riscv64@0.27.7':
    resolution: {integrity: sha512-hL25LbxO1QOngGzu2U5xeXtxXcW+/GvMN3ejANqXkxZ/opySAZMrc+9LY/WyjAan41unrR3YrmtTsUpwT66InQ==}
    engines: {node: '>=18'}
    cpu: [riscv64]
    os: [linux]

  '@esbuild/linux-s390x@0.27.7':
    resolution: {integrity: sha512-2k8go8Ycu1Kb46vEelhu1vqEP+UeRVj2zY1pSuPdgvbd5ykAw82Lrro28vXUrRmzEsUV0NzCf54yARIK8r0fdw==}
    engines: {node: '>=18'}
    cpu: [s390x]
    os: [linux]

  '@esbuild/linux-x64@0.27.7':
    resolution: {integrity: sha512-hzznmADPt+OmsYzw1EE33ccA+HPdIqiCRq7cQeL1Jlq2gb1+OyWBkMCrYGBJ+sxVzve2ZJEVeePbLM2iEIZSxA==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [linux]

  '@esbuild/netbsd-arm64@0.27.7':
    resolution: {integrity: sha512-b6pqtrQdigZBwZxAn1UpazEisvwaIDvdbMbmrly7cDTMFnw/+3lVxxCTGOrkPVnsYIosJJXAsILG9XcQS+Yu6w==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [netbsd]

  '@esbuild/netbsd-x64@0.27.7':
    resolution: {integrity: sha512-OfatkLojr6U+WN5EDYuoQhtM+1xco+/6FSzJJnuWiUw5eVcicbyK3dq5EeV/QHT1uy6GoDhGbFpprUiHUYggrw==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [netbsd]

  '@esbuild/openbsd-arm64@0.27.7':
    resolution: {integrity: sha512-AFuojMQTxAz75Fo8idVcqoQWEHIXFRbOc1TrVcFSgCZtQfSdc1RXgB3tjOn/krRHENUB4j00bfGjyl2mJrU37A==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [openbsd]

  '@esbuild/openbsd-x64@0.27.7':
    resolution: {integrity: sha512-+A1NJmfM8WNDv5CLVQYJ5PshuRm/4cI6WMZRg1by1GwPIQPCTs1GLEUHwiiQGT5zDdyLiRM/l1G0Pv54gvtKIg==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [openbsd]

  '@esbuild/openharmony-arm64@0.27.7':
    resolution: {integrity: sha512-+KrvYb/C8zA9CU/g0sR6w2RBw7IGc5J2BPnc3dYc5VJxHCSF1yNMxTV5LQ7GuKteQXZtspjFbiuW5/dOj7H4Yw==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [openharmony]

  '@esbuild/sunos-x64@0.27.7':
    resolution: {integrity: sha512-ikktIhFBzQNt/QDyOL580ti9+5mL/YZ
```


## File: SECURITY.md

```
# Security Policy

## Supported Versions

Please check the table below for the supported versions of AutoSkills that currently receive security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our project seriously. If you discover a security vulnerability in AutoSkills, please **DO NOT** open a public issue.

Instead, please report it privately to the maintainers to give us time to patch the issue before making it public.

1. Email the core maintainers directly or use GitHub's private vulnerability reporting feature (if enabled on the repository).
2. Provide a detailed summary of the vulnerability, including how to reproduce it and the potential impact.

You should receive a response within 48 hours. If the issue is confirmed, we will release a patch as quickly as possible and credit you for the discovery.

```


## File: tsconfig.json

```
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}

```


## File: .github/dependabot.yml

```
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "chore(deps)"
    labels:
      - "dependencies"

```


## File: .github/ISSUE_TEMPLATE/bug_report.yml

```
name: Bug Report
description: Create a report to help us improve
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to reproduce
      description: Exact steps to reproduce the issue.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: What OS, Node version, or browser were you using?

```


## File: .github/ISSUE_TEMPLATE/feature_request.yml

```
name: Feature Request
description: Suggest an idea for this project
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a new idea for AutoSkills!
  - type: textarea
    id: description
    attributes:
      label: Is your feature request related to a problem? Please describe.
      description: A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Describe the solution you'd like
      description: A clear and concise description of what you want to happen.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Describe alternatives you've considered
      description: A clear and concise description of any alternative solutions or features you've considered.

```


## File: .github/PULL_REQUEST_TEMPLATE.md

```
## What Changed

<!-- Describe the specific changes made in this PR -->

## Why This Change

<!-- Explain the motivation and context for this change -->

## Testing Done

<!-- Describe the testing you performed to validate your changes -->

- [ ] Manual testing completed
- [ ] Automated tests pass locally
- [ ] Edge cases considered and tested

## Type of Change

- [ ] `fix:` Bug fix
- [ ] `feat:` New feature
- [ ] `refactor:` Code refactoring
- [ ] `docs:` Documentation
- [ ] `test:` Tests
- [ ] `chore:` Maintenance/tooling

## Security & Quality Checklist

- [ ] No secrets or API keys committed
- [ ] Follows the project's coding standards
- [ ] No sensitive data exposed in logs or output

## Documentation

- [ ] Updated relevant documentation
- [ ] Added comments for complex logic
- [ ] README updated (if needed)

```


## File: .github/workflows/ci.yml

```
name: CLI

on:
  push:
    branches: [main]
    paths:
      - "packages/autoskills/**"
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Check linting
        run: pnpm run lint

      - name: Check formatting
        run: pnpm run fmt:check

  test:
    name: Tests
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        working-directory: packages/autoskills

      - name: Run tests
        run: pnpm test
        working-directory: packages/autoskills

```


## File: .github/workflows/compat.yml

```
name: Compatibility

on:
  workflow_run:
    workflows: [CLI]
    types: [completed]

permissions:
  contents: read

jobs:
  compat:
    name: Node ${{ matrix.node-version }} / ${{ matrix.os }}
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        node-version: [22]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha }}

      - uses: pnpm/action-setup@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        working-directory: packages/autoskills

      - name: Run tests
        run: pnpm test
        working-directory: packages/autoskills

      - name: E2E — install skills in fake project
        shell: bash
        run: |
          mkdir -p "$RUNNER_TEMP/test-project"
          echo '{ "dependencies": { "next": "15.0.0", "react": "19.0.0" } }' > "$RUNNER_TEMP/test-project/package.json"
          cd "$RUNNER_TEMP/test-project"
          node "$GITHUB_WORKSPACE/packages/autoskills/index.mjs" -y --verbose

```


## File: .github/workflows/issue-response-labels.yml

```
name: Issue response labels

on:
  issue_comment:
    types: [created]

permissions:
  issues: write

jobs:
  update-labels:
    if: >-
      !github.event.issue.pull_request &&
      github.event.comment.user.login == github.event.issue.user.login &&
      contains(github.event.issue.labels.*.name, 'waiting response')
    runs-on: ubuntu-latest
    steps:
      - name: Remove "waiting response" and add "more info provided"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh issue edit ${{ github.event.issue.number }} \
            --repo ${{ github.repository }} \
            --remove-label "waiting response" \
            --add-label "more info provided"

```


## File: .github/workflows/web.yml

```
name: Web

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "public/**"
      - "astro.config.mjs"
      - "package.json"
  pull_request:
    branches: [main]
    paths:
      - "src/**"
      - "public/**"
      - "astro.config.mjs"
      - "package.json"

permissions:
  contents: read

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build site
        run: pnpm run build

```


(… 23 more files omitted due to size limit)
<!-- fetched-content:end -->
