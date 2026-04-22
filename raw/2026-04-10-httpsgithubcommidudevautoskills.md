---
title: https://github.com/midudev/autoskills
type: url
captured: 2026-04-10 12:47:46.698486+00:00
source: android-share
url: https://github.com/midudev/autoskills
content_hash: sha256:57d993c267b81dfdfe1a246bd30d8a5b32ee9a40722a92ff3a4f90a7746f7cef
tags: []
status: ingested
last_refreshed: '2026-04-22T02:44:24+00:00'
---

https://github.com/midudev/autoskills

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:44:24+00:00
- source_url: https://github.com/midudev/autoskills
- resolved_url: https://github.com/midudev/autoskills
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: midudev/autoskills
Description: One command. Your entire AI skill stack. Installed.
Stars: 3566
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

Languages: TypeScript 72.0%, JavaScript 14.5%, Astro 10.5%, HTML 2.5%, CSS 0.5%

## Recent Releases

### v0.2.7 (2026-04-09)

### ✨ Features

- feat(autoskills): add TypeScript build step to compile .ts to dist/ [`7a0c570`](git+https://github.com/midudev/autoskills/commit/7a0c570)

### 🐛 Bug Fixes

- fix(autoskills): build before publish and fix test glob in release script [`4a324eb`](git+https://github.com/midudev/autoskills/commit/4a324eb)
- fix(autoskills): prefer compiled dist/main.js, fallback to .ts in dev [`ab9aa59`](git+https://github.com/midudev/autoskills/commit/ab9aa59)

### v0.2.6 (2026-04-09)

### ✨ Features

- feat: show structured error details in install summary [`64ed941`](git+https://github.com/midudev/autoskills/commit/64ed941)
- feat: add Laravel detection with multi-signal approach [`cc4f7c2`](git+https://github.com/midudev/autoskills/commit/cc4f7c2)
- feat(autoskills): add Python ecosystem technology detection (#17) [`323edbf`](git+https://github.com/midudev/autoskills/commit/323edbf)
- feat: add Electron project detection (#74) [`1d5bd1f`](git+https://github.com/midudev/autoskills/commit/1d5bd1f)
- feat: agregar detección de tecnologías y skills para proyectos Ruby on Rail…

### v0.2.4 (2026-04-06)

### ✨ Features

- feat(agents): add OpenCode detection [`4b0e23f`](git+https://github.com/midudev/autoskills/commit/4b0e23f)
- feat: pre-uncheck already installed skills in multi-select [`365e707`](git+https://github.com/midudev/autoskills/commit/365e707)
- chore: add benchmark script for performance measurement [`ab1c879`](git+https://github.com/midudev/autoskills/commit/ab1c879)
- feat: add Swift concurrency, Xcode build optimization, Swift Testing and Core Data skills [`1efdc8f`](git+https://github.com/midudev/autoskills/commit/1efdc8f)

### 🐛 Bug Fixes

- fix: resolve npm publish warnings …

### v0.2.3 (2026-04-04)

### ✨ Features

- refactor: add test helpers and reduce duplication across test files [`fdbb7af`](https://github.com/midudev/autoskills/commit/fdbb7af)
- feat: add Three.js and @react-three/fiber. [`6d5ac16`](https://github.com/midudev/autoskills/commit/6d5ac16)
- feat: add support for deno.json and deno.jsonc in workspace resolution and technology detection [`7d92dd1`](https://github.com/midudev/autoskills/commit/7d92dd1)
- docs: add Clerk and Spring Boot to supported technologies [`d5998e0`](https://github.com/midudev/autoskills/commit/d5998e0)
- feat: add Kiro agent support [`d5016c5`](http…

### v0.2.2 (2026-04-01)

### ✨ Features

- feat: simplificar la salida de detección de Cloudflare en pruebas de CLI [`cf190bd`](https://github.com/midudev/autoskills/commit/cf190bd)
- feat: mejorar la visualización en multiSelect al agregar separación entre grupos [`b11997d`](https://github.com/midudev/autoskills/commit/b11997d)
- feat: actualizar iconos en la salida de CLI para mejorar la legibilidad [`0c25238`](https://github.com/midudev/autoskills/commit/0c25238)
- feat: mejorar la visualización de etiquetas de habilidades en la salida de CLI [`41b0d48`](https://github.com/midudev/autoskills/commit/41b0d48)
- feat:…

## Recent Commits

- 2026-04-15 b511814 Miguel Ángel Durán: Merge pull request #82 from midudev/dependabot/npm_and_yarn/oxfmt-0.44.0
- 2026-04-15 7f4cd58 Miguel Ángel Durán (midudev): refactor(autoskills): clean up SKILLS_MAP by removing redundant skills entries
- 2026-04-15 0086d2b Miguel Ángel Durán: Merge pull request #85 from muhamadeissa92/support-aspnet-core
- 2026-04-15 add6015 Miguel Ángel Durán (midudev): Merge branch 'main' into dependabot/npm_and_yarn/oxfmt-0.44.0
- 2026-04-15 31430dd Miguel Ángel Durán (midudev): refactor(tests): streamline CLAUDE.md test case formatting
- 2026-04-15 b0633e5 Miguel Ángel Durán: Merge pull request #87 from pedrocastellanos/feat/add-react-hook-form-support
- 2026-04-14 7e91438 Pedro Castellanos Alonso: feat(autoskills): add React Hook Form support
- 2026-04-14 986b05b Miguel Ángel Durán (midudev): fix(autoskills): stop generating CLAUDE.md, clean up existing sections
- 2026-04-13 888353a Miguel Ángel Durán: Merge pull request #83 from midudev/dependabot/npm_and_yarn/oxlint-1.59.0
- 2026-04-13 9d62ab8 Miguel Ángel Durán: Merge pull request #84 from midudev/dependabot/npm_and_yarn/astro-6.1.5
- 2026-04-13 0149d2e Mohamed Eissa: style: format code with oxfmt
- 2026-04-13 198ff70 Mohamed Eissa: feat: add support for .NET, C#, ASP.NET Core, Blazor, and Minimal API
- 2026-04-12 fd2bd9a dependabot[bot]: chore(deps): bump astro from 6.1.3 to 6.1.5
- 2026-04-12 619ab8a dependabot[bot]: chore(deps): bump oxlint from 1.58.0 to 1.59.0
- 2026-04-12 e872ddc dependabot[bot]: chore(deps): bump oxfmt from 0.43.0 to 0.44.0
- 2026-04-12 0633c71 Miguel Ángel Durán (midudev): Merge branch 'main' of github.com:midudev/autoskills
- 2026-04-12 2e3784e Miguel Ángel Durán (midudev): chore: remove vercel.json configuration file
- 2026-04-12 55da656 Miguel Ángel Durán: Merge pull request #78 from pedrocastellanos/feat/add-zod-support
- 2026-04-10 3d05e4c Pedro Castellanos Alonso: feat(autoskills): add Zod support
- 2026-04-09 d3a03f2 Miguel Ángel Durán (midudev): chore: reorder package.json fields (engines after devDependencies)

## Open Issues (top 10)

- #89 [FEATURE] Refactorizar skills-map a arquitectura de plugins autosuficientes (by Angelito91)
- #93 [BUG] Failed to install pydantic skill (by miesgre)
- #92 [FEATURE] Add auto skill for .net (by jjj883831)

## Recently Merged PRs (top 10)

- #82 chore(deps): bump oxfmt from 0.43.0 to 0.44.0 (merged 2026-04-15)
- #85 Support DotNet,C# and Aspnet-core (merged 2026-04-15)
- #87 feat(autoskills): add React Hook Form support (merged 2026-04-15)
- #83 chore(deps): bump oxlint from 1.58.0 to 1.59.0 (merged 2026-04-13)
- #84 chore(deps): bump astro from 6.1.3 to 6.1.5 (merged 2026-04-13)
- #78 feat(autoskills): add Zod support (merged 2026-04-12)
- #17 feat(autoskills): add Python ecosystem technology detection (merged 2026-04-09)
- #57 fix: detect technologies in Gradle multi-module projects via settings gradle (#26) (merged 2026-04-09)
- #74 feat: add Electron project detection (merged 2026-04-09)
- #70 feat(detect): add Dart and Flutter project detection (merged 2026-04-09)


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


## File: packages/autoskills/.gitignore

```
dist/

```


## File: packages/autoskills/package.json

```
{
  "name": "autoskills",
  "version": "0.2.7",
  "description": "Auto-detect and install the best AI agent skills for your project",
  "keywords": [
    "agent",
    "ai",
    "auto",
    "claude",
    "cli",
    "copilot",
    "cursor",
    "detect",
    "skills"
  ],
  "homepage": "https://autoskills.sh",
  "license": "CC-BY-NC-4.0",
  "author": "midudev",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/midudev/autoskills.git"
  },
  "bin": {
    "autoskills": "index.mjs"
  },
  "files": [
    "index.mjs",
    "dist/"
  ],
  "type": "module",
  "scripts": {
    "build": "tsc",
    "test": "node --test 'tests/*.test.ts'",
    "release": "node scripts/release.mjs",
    "bench": "node scripts/bench.mjs"
  },
  "devDependencies": {
    "@types/node": "22.15.3",
    "typescript": "5.8.3"
  },
  "engines": {
    "node": ">=22.6.0"
  }
}

```


## File: packages/autoskills/pnpm-lock.yaml

```
lockfileVersion: '9.0'

settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

importers:

  .:
    devDependencies:
      '@types/node':
        specifier: 22.15.3
        version: 22.15.3
      typescript:
        specifier: 5.8.3
        version: 5.8.3

packages:

  '@types/node@22.15.3':
    resolution: {integrity: sha512-lX7HFZeHf4QG/J7tBZqrCAXwz9J5RD56Y6MpP0eJkka8p+K0RY/yBTW7CYFJ4VGCclxqOLKmiGP5juQc6MKgcw==}

  typescript@5.8.3:
    resolution: {integrity: sha512-p1diW6TqL9L07nNxvRMM7hMMw4c5XOo/1ibL4aAIGmSAt9slTE1Xgw5KWuof2uTOvCg9BY7ZRi+GaF+7sfgPeQ==}
    engines: {node: '>=14.17'}
    hasBin: true

  undici-types@6.21.0:
    resolution: {integrity: sha512-iwDZqg0QAGrg9Rav5H4n0M64c3mkR59cJ6wQp+7C4nI0gsmExaedaYLNO44eT4AtBBwjbTiGPMlt2Md0T9H9JQ==}

snapshots:

  '@types/node@22.15.3':
    dependencies:
      undici-types: 6.21.0

  typescript@5.8.3: {}

  undici-types@6.21.0: {}

```


## File: packages/autoskills/README.md

```
# autoskills

Auto-detect and install the best AI agent skills for your project. One command, zero config.

```bash
npx autoskills
```

`autoskills` scans your project, detects the technologies you use, and installs curated [AI agent skills](https://skills.sh) that make Cursor, Claude Code, and other AI coding assistants actually understand your stack.

## Quick Start

Run it in your project root:

```bash
npx autoskills
```

That's it. It will:

1. **Scan** your `package.json`, config files, and project structure
2. **Detect** every technology in your stack
3. **Show** an interactive selector with the best skills for your project
4. **Install** them in parallel with live progress
5. **Generate `CLAUDE.md` automatically** when Claude Code is one of the target agents

### Skip the prompt

```bash
npx autoskills -y
```

### Preview without installing

```bash
npx autoskills --dry-run
```

### Claude Code summary

If `claude-code` is auto-detected or passed with `-a`, `autoskills` writes a `CLAUDE.md` file in your project root summarizing the markdown files installed under `.claude/skills`.

## Options

| Flag              | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `-y`, `--yes`     | Skip confirmation prompt, install all detected skills |
| `--dry-run`       | Show detected skills without installing anything      |
| `-v`, `--verbose` | Show error details if any installation fails          |
| `-h`, `--help`    | Show help message                                     |

## Supported Technologies

`autoskills` detects **50+ technologies** from your `package.json`, lockfiles, Gradle files, and config files:

### Frameworks & Libraries

| Technology           | Detected from                                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| React                | `react`, `react-dom` packages                                                                                                                     |
| Next.js              | `next` package or `next.config.*`                                                                                                                 |
| Vue                  | `vue` package                                                                                                                                     |
| Nuxt                 | `nuxt` package or `nuxt.config.*`                                                                                                                 |
| Svelte               | `svelte`, `@sveltejs/kit` or `svelte.config.js`                                                                                                   |
| Angular              | `@angular/core` or `angular.json`                                                                                                                 |
| Astro                | `astro` package or `astro.config.*`                                                                                                               |
| Expo                 | `expo` package                                                                                                                                    |
| React Native         | `react-native` package                                                                                                                            |
| Flutter              | `pubspec.yaml` file with `flutter:` key                                                                                                           |
| Kotlin Multiplatform | Gradle with KMP plugin: `kotlin("multiplatform")`, `org.jetbrains.kotlin.multiplatform`, or `kotlin-multiplatform` in `gradle/libs.versions.toml` |
| Android              | Gradle with `com.android.application`, `com.android.library`, or `com.android.kotlin.multiplatform.library`                                       |
| Remotion             | `remotion`, `@remotion/cli`                                                                                                                       |
| GSAP                 | `gsap` package                                                                                                                                    |
| Three.js             | `three`, `@react-three/fiber`, `@react-three/drei`                                                                                                |
| Express              | `express` package                                                                                                                                 |
| Hono                 | `hono` package                                                                                                                                    |
| NestJS               | `@nestjs/core` package                                                                                                                            |
| Spring Boot          | Gradle with `spring-boot-starter` or `org.springframework.boot`                                                                                   |
| ASP.NET Core         | `.csproj` file with `Microsoft.NET.Sdk.Web`                                                                                                       |
| Blazor               | `.csproj` with `Microsoft.NET.Sdk.BlazorWebAssembly` or `Microsoft.AspNetCore.Components`                                                         |
| ASP.NET Minimal API  | `.csproj` with `Microsoft.AspNetCore.OpenApi` or `Swashbuckle.AspNetCore`                                                                         |

### Styling & UI

| Technology   | Detected from                                             |
| ------------ | --------------------------------------------------------- |
| Tailwind CSS | `tailwindcss`, `@tailwindcss/vite` or `tailwind.config.*` |
| shadcn/ui    | `components.json`                                         |

### Runtimes & Tooling

| Technology | Detected from                                                |
| ---------- | ------------------------------------------------------------ |
| TypeScript | `typescript` package or `tsconfig.json`                      |
| Node.js    | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `.nvmrc` |
| Bun        | `bun.lockb`, `bun.lock`, `bunfig.toml`                       |
| Deno       | `deno.json`, `deno.jsonc`, `deno.lock`                       |
| Dart       | `pubspec.yaml`                                               |
| Go         | `go.mod`, `go.work`                                          |
| Vite       | `vite` package or `vite.config.*`                            |
| Turborepo  | `turbo` package or `turbo.json`                              |
| Vitest     | `vitest` package or `vitest.config.*`                        |
| oxlint     | `oxlint` package or `.oxlintrc.json`                         |
| .NET       | `global.json`, `NuGet.Config`, `*.csproj`, `*.sln`           |
| C#         | `*.csproj`, `*.sln`                                          |

### Backend & Data

| Technology      | Detected from                                            |
| --------------- | -------------------------------------------------------- |
| Supabase        | `@supabase/supabase-js`, `@supabase/ssr`                 |
| Zod             | `zod` package                                            |
| React Hook Form | `react-hook-form` package                                |
| Neon Postgres   | `@neondatabase/serverless`                               |
| Prisma          | `prisma`, `@prisma/client`                               |
| Drizzle ORM     | `drizzle-orm`, `drizzle-kit`                             |
| Stripe          | `stripe`, `@stripe/stripe-js`, `@stripe/react-stripe-js` |
| Better Auth     | `better-auth` package                                    |

### Authentication

| Technology | Detected from                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Clerk      | `@clerk/nextjs`, `@clerk/react`, `@clerk/expo`, `@clerk/astro`, `@clerk/remix`, `@clerk/vue`, or any `@clerk/*` scope |

### Cloud & Deploy

| Technology        | Detected from                                        |
| ----------------- | ---------------------------------------------------- |
| Vercel            | `vercel.json`, `.vercel/`, `@astrojs/vercel`         |
| Cloudflare        | `wrangler`, `wrangler.toml`, `@astrojs/cloudflare`   |
| Cloudflare Agents | `agents` package                                     |
| Cloudflare AI     | `@cloudflare/ai` or AI binding in `wrangler.json`    |
| Durable Objects   | `durable_objects` in `wrangler.json`/`wrangler.toml` |
| Azure             | `@azure/*` packages                                  |
| AWS               | `@aws-sdk/*`, `aws-cdk*` packages                    |

### AI

| Technology    | Detected from                                                 |
| ------------- | ------------------------------------------------------------- |
| Vercel AI SDK | `ai`, `@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/google` |
| ElevenLabs    | `elevenlabs` package                                          |

### Other

| Technology | Detected from                                                                               |
| ---------- | ------------------------------------------------------------------------------------------- |
| Playwright | `@playwright/test`, `playwright` or `playwright.config.*`                                   |
| SwiftUI    | `Package.swift`                                                                             |
| WordPress  | `wp-config.php`, `@wordpress/*`, `composer.json` with wpackagist, theme `style.css`         |
| Tauri      | `@tauri-apps/api`, `@tauri-apps/cli` or `src-tauri/tauri.conf.json`                         |
| Electron   | `electron` package, `electron-builder.yml`, `forge.config.js`, or `electron-vite.config.ts` |

### Web Frontend Detection

Even without a framework, `autoskills` scans your file tree for web frontend signals (`.html`, `.css`, `.scss`, `.vue`, `.svelte`, `.jsx`, `.tsx`, `.twig`, `.blade.php`, etc.) and installs skills for frontend design, accessibility, and SEO.

## Combo Detection

When multiple technologies are used together, `autoskills` detects **technology combos** and adds specialized skills for the combination:

- **Next.js + Supabase** — Supabase Postgres best practices for Next.js
- **Next.js + Vercel AI SDK** — AI SDK patterns with Next.js
- **Next.js + Playwright** — E2E testing best practices for Next.js
- **React + shadcn/ui** — shadcn component patterns with React
- **Tailwind CSS + shadcn/ui** — Tailwind v4 + shadcn integration
- **Expo + Tailwind CSS** — Tailwind setup for Expo
- **React Native + Expo** — Native UI patterns
- **React Hook Form + Zod** — Form validation patterns with Zod schemas
- **GSAP + React** — GSAP animation patterns in React
- **Cloudflare + Vite** — Vinext migration guide
- **Node.js + Express** — Express server patterns

## How It Works

`autoskills` uses [skills.sh](https://skills.sh) under the hood — the open skill registry for AI coding agents. Skills are markdown files that teach AI assistants how to work with specific technologies, following best practices and patterns from the official maintainers.

The detection runs entirely locally with zero network requests until installation begins.

## Requirements

- Node.js >= 22.0.0

## License

CC-BY-NC-4.0 — Created by [@midudev](https://github.com/midudev)

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
    resolution: {integrity: sha512-ikktIhFBzQNt/QDyOL580ti9+5mL/YZeUPKU2ivGtGjdTYoqz6jObj6nOMfhASpS4GU4Q/Clh1QtxWAvcYKamA==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [sunos]

  '@esbuild/win32-arm64@0.27.7':
    resolution: {integrity: sha512-7yRhbHvPqSpRUV7Q20VuDwbjW5kIMwTHpptuUzV+AA46kiPze5Z7qgt6CLCK3pWFrHeNfDd1VKgyP4O+ng17CA==}
    engines: {node: '>=18'}
    cpu: [arm64]
    os: [win32]

  '@esbuild/win32-ia32@0.27.7':
    resolution: {integrity: sha512-SmwKXe6VHIyZYbBLJrhOoCJRB/Z1tckzmgTLfFYOfpMAx63BJEaL9ExI8x7v0oAO3Zh6D/Oi1gVxEYr5oUCFhw==}
    engines: {node: '>=18'}
    cpu: [ia32]
    os: [win32]

  '@esbuild/win32-x64@0.27.7':
    resolution: {integrity: sha512-56hiAJPhwQ1R4i+21FVF7V8kSD5zZTdHcVuRFMW0hn753vVfQN8xlx4uOPT4xoGH0Z/oVATuR82AiqSTDIpaHg==}
    engines: {node: '>=18'}
    cpu: [x64]
    os: [win32]

  '@img/colour@1.1.0':
    resolution: {integrity: sha512-Td76q7j57o/tLVdgS746cYARfSyxk8iEfRxewL9h4OMzYhbW4TAcppl0mT4eyqXddh6L/jwoM75mo7ixa/pCeQ==}
    engines: {node: '>=18'}

  '@img/sharp-darwin-arm64@0.34.5':
    resolution: {integrity: sha512-imtQ3WMJXbMY4fxb/Ndp6HBTNVtWCUI0WdobyheGf5+ad6xX8VIDO8u2xE4qc/fr08CKG/7dDseFtn6M6g/r3w==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [arm64]
    os: [darwin]

  '@img/sharp-darwin-x64@0.34.5':
    resolution: {integrity: sha512-YNEFAF/4KQ/PeW0N+r+aVVsoIY0/qxxikF2SWdp+NRkmMB7y9LBZAVqQ4yhGCm/H3H270OSykqmQMKLBhBJDEw==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [x64]
    os: [darwin]

  '@img/sharp-libvips-darwin-arm64@1.2.4':
    resolution: {integrity: sha512-zqjjo7RatFfFoP0MkQ51jfuFZBnVE2pRiaydKJ1G/rHZvnsrHAOcQALIi9sA5co5xenQdTugCvtb1cuf78Vf4g==}
    cpu: [arm64]
    os: [darwin]

  '@img/sharp-libvips-darwin-x64@1.2.4':
    resolution: {integrity: sha512-1IOd5xfVhlGwX+zXv2N93k0yMONvUlANylbJw1eTah8K/Jtpi15KC+WSiaX/nBmbm2HxRM1gZ0nSdjSsrZbGKg==}
    cpu: [x64]
    os: [darwin]

  '@img/sharp-libvips-linux-arm64@1.2.4':
    resolution: {integrity: sha512-excjX8DfsIcJ10x1Kzr4RcWe1edC9PquDRRPx3YVCvQv+U5p7Yin2s32ftzikXojb1PIFc/9Mt28/y+iRklkrw==}
    cpu: [arm64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linux-arm@1.2.4':
    resolution: {integrity: sha512-bFI7xcKFELdiNCVov8e44Ia4u2byA+l3XtsAj+Q8tfCwO6BQ8iDojYdvoPMqsKDkuoOo+X6HZA0s0q11ANMQ8A==}
    cpu: [arm]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linux-ppc64@1.2.4':
    resolution: {integrity: sha512-FMuvGijLDYG6lW+b/UvyilUWu5Ayu+3r2d1S8notiGCIyYU/76eig1UfMmkZ7vwgOrzKzlQbFSuQfgm7GYUPpA==}
    cpu: [ppc64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linux-riscv64@1.2.4':
    resolution: {integrity: sha512-oVDbcR4zUC0ce82teubSm+x6ETixtKZBh/qbREIOcI3cULzDyb18Sr/Wcyx7NRQeQzOiHTNbZFF1UwPS2scyGA==}
    cpu: [riscv64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linux-s390x@1.2.4':
    resolution: {integrity: sha512-qmp9VrzgPgMoGZyPvrQHqk02uyjA0/QrTO26Tqk6l4ZV0MPWIW6LTkqOIov+J1yEu7MbFQaDpwdwJKhbJvuRxQ==}
    cpu: [s390x]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linux-x64@1.2.4':
    resolution: {integrity: sha512-tJxiiLsmHc9Ax1bz3oaOYBURTXGIRDODBqhveVHonrHJ9/+k89qbLl0bcJns+e4t4rvaNBxaEZsFtSfAdquPrw==}
    cpu: [x64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-libvips-linuxmusl-arm64@1.2.4':
    resolution: {integrity: sha512-FVQHuwx1IIuNow9QAbYUzJ+En8KcVm9Lk5+uGUQJHaZmMECZmOlix9HnH7n1TRkXMS0pGxIJokIVB9SuqZGGXw==}
    cpu: [arm64]
    os: [linux]
    libc: [musl]

  '@img/sharp-libvips-linuxmusl-x64@1.2.4':
    resolution: {integrity: sha512-+LpyBk7L44ZIXwz/VYfglaX/okxezESc6UxDSoyo2Ks6Jxc4Y7sGjpgU9s4PMgqgjj1gZCylTieNamqA1MF7Dg==}
    cpu: [x64]
    os: [linux]
    libc: [musl]

  '@img/sharp-linux-arm64@0.34.5':
    resolution: {integrity: sha512-bKQzaJRY/bkPOXyKx5EVup7qkaojECG6NLYswgktOZjaXecSAeCWiZwwiFf3/Y+O1HrauiE3FVsGxFg8c24rZg==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [arm64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linux-arm@0.34.5':
    resolution: {integrity: sha512-9dLqsvwtg1uuXBGZKsxem9595+ujv0sJ6Vi8wcTANSFpwV/GONat5eCkzQo/1O6zRIkh0m/8+5BjrRr7jDUSZw==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [arm]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linux-ppc64@0.34.5':
    resolution: {integrity: sha512-7zznwNaqW6YtsfrGGDA6BRkISKAAE1Jo0QdpNYXNMHu2+0dTrPflTLNkpc8l7MUP5M16ZJcUvysVWWrMefZquA==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [ppc64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linux-riscv64@0.34.5':
    resolution: {integrity: sha512-51gJuLPTKa7piYPaVs8GmByo7/U7/7TZOq+cnXJIHZKavIRHAP77e3N2HEl3dgiqdD/w0yUfiJnII77PuDDFdw==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [riscv64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linux-s390x@0.34.5':
    resolution: {integrity: sha512-nQtCk0PdKfho3eC5MrbQoigJ2gd1CgddUMkabUj+rBevs8tZ2cULOx46E7oyX+04WGfABgIwmMC0VqieTiR4jg==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [s390x]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linux-x64@0.34.5':
    resolution: {integrity: sha512-MEzd8HPKxVxVenwAa+JRPwEC7QFjoPWuS5NZnBt6B3pu7EG2Ge0id1oLHZpPJdn3OQK+BQDiw9zStiHBTJQQQQ==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [x64]
    os: [linux]
    libc: [glibc]

  '@img/sharp-linuxmusl-arm64@0.34.5':
    resolution: {integrity: sha512-fprJR6GtRsMt6Kyfq44IsChVZeGN97gTD331weR1ex1c1rypDEABN6Tm2xa1wE6lYb5DdEnk03NZPqA7Id21yg==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [arm64]
    os: [linux]
    libc: [musl]

  '@img/sharp-linuxmusl-x64@0.34.5':
    resolution: {integrity: sha512-Jg8wNT1MUzIvhBFxViqrEhWDGzqymo3sV7z7ZsaWbZNDLXRJZoRGrjulp60YYtV4wfY8VIKcWidjojlLcWrd8Q==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [x64]
    os: [linux]
    libc: [musl]

  '@img/sharp-wasm32@0.34.5':
    resolution: {integrity: sha512-OdWTEiVkY2PHwqkbBI8frFxQQFekHaSSkUIJkwzclWZe64O1X4UlUjqqqLaPbUpMOQk6FBu/HtlGXNblIs0huw==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [wasm32]

  '@img/sharp-win32-arm64@0.34.5':
    resolution: {integrity: sha512-WQ3AgWCWYSb2yt+IG8mnC6Jdk9Whs7O0gxphblsLvdhSpSTtmu69ZG1Gkb6NuvxsNACwiPV6cNSZNzt0KPsw7g==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [arm64]
    os: [win32]

  '@img/sharp-win32-ia32@0.34.5':
    resolution: {integrity: sha512-FV9m/7NmeCmSHDD5j4+4pNI8Cp3aW+JvLoXcTUo0IqyjSfAZJ8dIUmijx1qaJsIiU+Hosw6xM5KijAWRJCSgNg==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [ia32]
    os: [win32]

  '@img/sharp-win32-x64@0.34.5':
    resolution: {integrity: sha512-+29YMsqY2/9eFEiW93eqWnuLcWcufowXewwSNIT6UwZdUUCrM3oFjMWH/Z6/TMmb4hlFenmfAVbpWeup2jryCw==}
    engines: {node: ^18.17.0 || ^20.3.0 || >=21.0.0}
    cpu: [x64]
    os: [win32]

  '@jridgewell/gen-mapping@0.3.13':
    resolution: {integrity: sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==}

  '@jridgewell/remapping@2.3.5':
    resolution: {integrity: sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==}

  '@jridgewell/resolve-uri@3.1.2':
    resolution: {integrity: sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==}
    engines: {node: '>=6.0.0'}

  '@jridgewell/sourcemap-codec@1.5.5':
    resolution: {integrity: sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==}

  '@jridgewell/trace-mapping@0.3.31':
    resolution: {integrity: sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==}

  '@next/env@16.2.1':
    resolution: {integrity: sha512-n8P/HCkIWW+gVal2Z8XqXJ6aB3J0tuM29OcHpCsobWlChH/SITBs1DFBk/HajgrwDkqqBXPbuUuzgDvUekREPg==}

  '@next/swc-darwin-arm64@16.2.1':
    resolution: {integrity: sha512-BwZ8w8YTaSEr2HIuXLMLxIdElNMPvY9fLqb20LX9A9OMGtJilhHLbCL3ggyd0TwjmMcTxi0XXt+ur1vWUoxj2Q==}
    engines: {node: '>= 10'}
    cpu: [arm64]
    os: [darwin]

  '@next/swc-darwin-x64@16.2.1':
    resolution: {integrity: sha512-/vrcE6iQSJq3uL3VGVHiXeaKbn8Es10DGTGRJnRZlk
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


## File: .vscode/extensions.json

```
{
  "recommendations": ["astro-build.astro-vscode"],
  "unwantedRecommendations": []
}

```


## File: .vscode/launch.json

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "command": "./node_modules/.bin/astro dev",
      "name": "Development server",
      "request": "launch",
      "type": "node-terminal"
    }
  ]
}

```


## File: packages/autoskills/CHANGELOG.md

```
# Changelog

## [0.2.7](git+https://github.com/midudev/autoskills/releases/tag/v0.2.7) (2026-04-09)

### ✨ Features

- feat(autoskills): add TypeScript build step to compile .ts to dist/ [`7a0c570`](git+https://github.com/midudev/autoskills/commit/7a0c570)

### 🐛 Bug Fixes

- fix(autoskills): build before publish and fix test glob in release script [`4a324eb`](git+https://github.com/midudev/autoskills/commit/4a324eb)
- fix(autoskills): prefer compiled dist/main.js, fallback to .ts in dev [`ab9aa59`](git+https://github.com/midudev/autoskills/commit/ab9aa59)

## [0.2.6](git+https://github.com/midudev/autoskills/releases/tag/v0.2.6) (2026-04-09)

### ✨ Features

- feat: show structured error details in install summary [`64ed941`](git+https://github.com/midudev/autoskills/commit/64ed941)
- feat: add Laravel detection with multi-signal approach [`cc4f7c2`](git+https://github.com/midudev/autoskills/commit/cc4f7c2)
- feat(autoskills): add Python ecosystem technology detection (#17) [`323edbf`](git+https://github.com/midudev/autoskills/commit/323edbf)
- feat: add Electron project detection (#74) [`1d5bd1f`](git+https://github.com/midudev/autoskills/commit/1d5bd1f)
- feat: agregar detección de tecnologías y skills para proyectos Ruby on Rails [`0987c24`](git+https://github.com/midudev/autoskills/commit/0987c24)
- feat(detect): add Dart and Flutter project detection (#70) [`7b5b2b3`](git+https://github.com/midudev/autoskills/commit/7b5b2b3)
- feat: generate CLAUDE.md summary for Claude Code installs (#61) [`60e8db8`](git+https://github.com/midudev/autoskills/commit/60e8db8)
- feat(detect): expand technology signals and combo mappings [`815f25f`](git+https://github.com/midudev/autoskills/commit/815f25f)
- feat(clerk): add new skills and framework combos [`ae23db2`](git+https://github.com/midudev/autoskills/commit/ae23db2)
- feat: add Rust technology detection from Cargo.toml [`0253ec4`](git+https://github.com/midudev/autoskills/commit/0253ec4)
- feat: add Go curated skills [`2be15ab`](git+https://github.com/midudev/autoskills/commit/2be15ab)
- feat: detect Go projects [`b7a43e8`](git+https://github.com/midudev/autoskills/commit/b7a43e8)

### 🐛 Bug Fixes

- fix: remove unused variable in claude.ts [`447b954`](git+https://github.com/midudev/autoskills/commit/447b954)
- fix: improve Gradle module parsing and update Laravel detection [`ff792ee`](git+https://github.com/midudev/autoskills/commit/ff792ee)
- fix: format code for better readability in collectMarkdownFiles and test cases [`7371088`](git+https://github.com/midudev/autoskills/commit/7371088)
- fix: handle escape sequences and batched input in multiSelect [`2c4b7fd`](git+https://github.com/midudev/autoskills/commit/2c4b7fd)
- fix: improve CLAUDE.md generation with symlink support and frontmatter parsing [`c661ed3`](git+https://github.com/midudev/autoskills/commit/c661ed3)
- fix: use delimited sections in CLAUDE.md to preserve user content [`55d4d05`](git+https://github.com/midudev/autoskills/commit/55d4d05)
- fix: detect technologies in Gradle multi-module projects via settings.gradle (#26) [`286494c`](git+https://github.com/midudev/autoskills/commit/286494c)

### 📦 Other Changes

- refactor: migrate autoskills package from .mjs to TypeScript [`1885540`](git+https://github.com/midudev/autoskills/commit/1885540)
- Merge pull request #57 from oscaruiz/fix/26-gradle-multimodule-detection [`9f1330f`](git+https://github.com/midudev/autoskills/commit/9f1330f)
- refactor: apply review improvements to Ruby/Rails detection [`027d3e9`](git+https://github.com/midudev/autoskills/commit/027d3e9)
- chore: bump version to 0.2.5 [`c51559b`](git+https://github.com/midudev/autoskills/commit/c51559b)
- chore: format (#66) [`4fc16a4`](git+https://github.com/midudev/autoskills/commit/4fc16a4)
- Merge branch 'main' into feat/go-support [`c4b7526`](git+https://github.com/midudev/autoskills/commit/c4b7526)
- terraform detection and skills added [`a49969a`](git+https://github.com/midudev/autoskills/commit/a49969a)
- Merge branch 'main' of github.com:midudev/autoskills [`4b08c10`](git+https://github.com/midudev/autoskills/commit/4b08c10)
- test(detect): cover new detections and Clerk combos [`3382bd7`](git+https://github.com/midudev/autoskills/commit/3382bd7)

## [0.2.4](git+https://github.com/midudev/autoskills/releases/tag/v0.2.4) (2026-04-06)

### ✨ Features

- feat(agents): add OpenCode detection [`4b0e23f`](git+https://github.com/midudev/autoskills/commit/4b0e23f)
- feat: pre-uncheck already installed skills in multi-select [`365e707`](git+https://github.com/midudev/autoskills/commit/365e707)
- chore: add benchmark script for performance measurement [`ab1c879`](git+https://github.com/midudev/autoskills/commit/ab1c879)
- feat: add Swift concurrency, Xcode build optimization, Swift Testing and Core Data skills [`1efdc8f`](git+https://github.com/midudev/autoskills/commit/1efdc8f)

### 🐛 Bug Fixes

- fix: resolve npm publish warnings that stripped bin entry [`c76623b`](git+https://github.com/midudev/autoskills/commit/c76623b)
- fix(agents): map .kiro folder to kiro-cli identifier [`36da4d8`](git+https://github.com/midudev/autoskills/commit/36da4d8)
- fix: resolve eslint warnings (unused imports, catch param, regex escape) [`db69e54`](git+https://github.com/midudev/autoskills/commit/db69e54)
- fix: changelog markdown link formatting [`b36f24f`](git+https://github.com/midudev/autoskills/commit/b36f24f)

### 📦 Other Changes

- chore: track pnpm-lock.yaml for deterministic installs [`0c94654`](git+https://github.com/midudev/autoskills/commit/0c94654)
- refactor: accept options object in collectSkills and improve multiSelect UX [`ba9028a`](git+https://github.com/midudev/autoskills/commit/ba9028a)
- Merge pull request #38 from Mo3oDev/fix/kiro-cli-agent-id [`8b06245`](git+https://github.com/midudev/autoskills/commit/8b06245)
- Merge pull request #33 from pol-cova/feat/ios-dev-skills [`9af064f`](git+https://github.com/midudev/autoskills/commit/9af064f)
- style: format code with consistent line wrapping and whitespace [`3b60dcc`](git+https://github.com/midudev/autoskills/commit/3b60dcc)
- perf: optimize installation phase with bin pre-warm, concurrency and repo sorting [`76c3ede`](git+https://github.com/midudev/autoskills/commit/76c3ede)
- perf: optimize detection phase with cached reads, Set lookups and reduced syscalls [`de3e835`](git+https://github.com/midudev/autoskills/commit/de3e835)

## [0.2.3](https://github.com/midudev/autoskills/releases/tag/v0.2.3) (2026-04-04)

### ✨ Features

- refactor: add test helpers and reduce duplication across test files `[fdbb7af](https://github.com/midudev/autoskills/commit/fdbb7af)`
- feat: add Three.js and @react-three/fiber. `[6d5ac16](https://github.com/midudev/autoskills/commit/6d5ac16)`
- feat: add support for deno.json and deno.jsonc in workspace resolution and technology detection `[7d92dd1](https://github.com/midudev/autoskills/commit/7d92dd1)`
- docs: add Clerk and Spring Boot to supported technologies `[d5998e0](https://github.com/midudev/autoskills/commit/d5998e0)`
- feat: add Kiro agent support `[d5016c5](https://github.com/midudev/autoskills/commit/d5016c5)`
- feat: add clerk router skill to nextjs-clerk combo `[bec0f69](https://github.com/midudev/autoskills/commit/bec0f69)`
- feat: add Clerk authentication detection and skills `[abfd4e5](https://github.com/midudev/autoskills/commit/abfd4e5)`

### 🐛 Bug Fixes

- style: fix oxfmt formatting `[4566573](https://github.com/midudev/autoskills/commit/4566573)`

### 📦 Other Changes

- refactor: use if-return instead of switch in bumpVersion `[4ffb3d0](https://github.com/midudev/autoskills/commit/4ffb3d0)`
- refactor: extract log/write aliases to replace console.log and process.stdout.write `[3a8961f](https://github.com/midudev/autoskills/commit/3a8961f)`
- Merge pull request #30 from pedrocastellanos/feat-add-threejs-react-three `[9aa3b4d](https://github.com/midudev/autoskills/commit/9aa3b4d)`
- Merge pull request #32 from John7bigo/feat/read-deno-json `[980e8f1](https://github.com/midudev/autoskills/commit/980e8f1)`
- Merge pull request #27 from Railly/feat/add-icons-and-docs `[4f4e61d](https://github.com/midudev/autoskills/commit/4f4e61d)`
- chore: lint and format before release `[e63bada](https://github.com/midudev/autoskills/commit/e63bada)`

## [0.2.2](https://github.com/midudev/autoskills/releases/tag/v0.2.2) (2026-04-01)

### ✨ Features

- feat: simplificar la salida de detección de Cloudflare en pruebas de CLI `[cf190bd](https://github.com/midudev/autoskills/commit/cf190bd)`
- feat: mejorar la visualización en multiSelect al agregar separación entre grupos `[b11997d](https://github.com/midudev/autoskills/commit/b11997d)`
- feat: actualizar iconos en la salida de CLI para mejorar la legibilidad `[0c25238](https://github.com/midudev/autoskills/commit/0c25238)`
- feat: mejorar la visualización de etiquetas de habilidades en la salida de CLI `[41b0d48](https://github.com/midudev/autoskills/commit/41b0d48)`
- feat: implementar rollback en caso de fallos durante el proceso de release `[013702f](https://github.com/midudev/autoskills/commit/013702f)`

## [0.2.1](https://github.com/midudev/autoskills/releases/tag/v0.2.1) (2026-04-01)

### ✨ Features

- feat: auto-detect installed agents when no -a flag is provided `[0b6c88c](https://github.com/midudev/autoskills/commit/0b6c88c)`
- feat: add Prisma, Stripe, Hono, Vitest, Drizzle, NestJS and Tauri to skills map `[ba11178](https://github.com/midudev/autoskills/commit/ba11178)`
- Add Svelte skills to skills-map `[a212de1](https://github.com/midudev/autoskills/commit/a212de1)`
- feat: update SKILLS_MAP to include new Angular skills `[d33c8db](https://github.com/midudev/autoskills/commit/d33c8db)`

### 📦 Other Changes

- Refactor transition properties in global.css for improved readability `[f1836fa](https://github.com/midudev/autoskills/commit/f1836fa)`
- Merge pull request #15 from vgpastor/feat/auto-detect-agents `[4ad60cc](https://github.com/midudev/autoskills/commit/4ad60cc)`
- Merge pull request #13 from PMFrancisco/feat/add-js-ecosystem-skills `[62a2879](https://github.com/midudev/autoskills/commit/62a2879)`

## [0.2.0](https://github.com/midudev/autoskills/releases/tag/v0.2.0) (2026-03-31)

### ✨ Features

- feat: add Java/Spring Boot detection and extract skills map to dedicated file `[90bd791](https://github.com/midudev/autoskills/commit/90bd791)`
- feat: add monorepo workspace detection support `[85e14cd](https://github.com/midudev/autoskills/commit/85e14cd)`
- feat(autoskills): detect Kotlin Multiplatform and Android via Gradle `[4efd5c9](https://github.com/midudev/autoskills/commit/4efd5c9)`
- Update autoskills package to version 0.1.6 and add release script `[92216ec](https://github.com/midudev/autoskills/commit/92216ec)`
- Add CHANGELOG.md for autoskills package `[03127c4](https://github.com/midudev/autoskills/commit/03127c4)`

### 🐛 Bug Fixes

- fix: hide combo source labels from skill list display `[138a895](https://github.com/midudev/autoskills/commit/138a895)`
- fix: Windows installer by making the npx spawn options platform-aware. `[b661b88](https://github.com/midudev/autoskills/commit/b661b88)`

### 📦 Other Changes

- Enhance release script documentation with JSDoc comments. Added detailed descriptions for changelog generation and update functions to improve clarity and maintainability. `[dbab11d](https://github.com/midudev/autoskills/commit/dbab11d)`
- Enhance documentation with JSDoc comments across multiple files. Added detailed descriptions for functions in index.mjs, installer.mjs, lib.mjs, ui.mjs, and release.mjs to improve code clarity and maintainability. `[595bfa0](https://github.com/midudev/autoskills/commit/595bfa0)`
- merge: resolve conflicts with main branch `[97c4cef](https://github.com/midudev/autoskills/commit/97c4cef)`
- merge: resolve conflicts with main branch `[9505993](https://github.com/midudev/autoskills/commit/9505993)`
- Merge pull request #10 from dieguedev/main `[31d4727](https://github.com/midudev/autoskills/commit/31d4727)`
- Merge pull request #6 from sebastiansandoval27/main `[70ca7fb](https://github.com/midudev/autoskills/commit/70ca7fb)`
- Merge pull request #3 from AlvaroMinarro/feat/kmp-android-detection `[2381250](https://github.com/midudev/autoskills/commit/2381250)`
- refactor(lib.mjs): Replace outdated tailwind-v4-shadcn SKILL `[d7e01a8](https://github.com/midudev/autoskills/commit/d7e01a8)`
- Enhance agent installation support in autoskills CLI `[0f90d9b](https://github.com/midudev/autoskills/commit/0f90d9b)`

## [0.1.6](https://github.com/midudev/autoskills/releases/tag/v0.1.6) (2026-03-30)

### 🐛 Bug Fixes

- Fix Windows npx spawn in installer `[ec48abb](https://github.com/midudev/autoskills/commit/ec48abb)`

## [0.1.5](https://github.com/midudev/autoskills/releases/tag/v0.1.5) (2026-03-30)

### 🐛 Bug Fixes

- Correct repository URL `[6f82a1a](https://github.com/midudev/autoskills/commit/6f82a1a)`

## [0.1.4](https://github.com/midudev/autoskills/releases/tag/v0.1.4) (2026-03-30)

### 📦 Other Changes

- Add README.md for autoskills package `[0471cfb](https://github.com/midudev/autoskills/commit/0471cfb)`

## [0.1.3](https://github.com/midudev/autoskills/releases/tag/v0.1.3) (2026-03-30)

### ✨ Features

- Add WordPress detection and enhance web frontend identification `[3804a8d](https://github.com/midudev/autoskills/commit/3804a8d)`
- Add Node.js and Express detection with backend skills `[f68da3c](https://github.com/midudev/autoskills/commit/f68da3c)`
- Add Deno detection with 6 skills `[393fc9e](https://github.com/midudev/autoskills/commit/393fc9e)`
- Add Bun detection and support for URL-based skills `[ae69f8c](https://github.com/midudev/autoskills/commit/ae69f8c)`
- Add GSAP, Pinia, Cloudflare smart detection and new skills `[0687302](https://github.com/midudev/autoskills/commit/0687302)`
- Add Pinia, Astro and oxlint skills support `[747bfc8](https://github.com/midudev/autoskills/commit/747bfc8)`
- Detect Vercel and Cloudflare from Astro adapters `[7d1be35](https://github.com/midudev/autoskills/commit/7d1be35)`
- Add gray color support to autoskills CLI `[a0b26ce](https://github.com/midudev/autoskills/commit/a0b26ce)`
- Add pink color support and sponsor message in CLI output `[6d21987](https://github.com/midudev/autoskills/commit/6d21987)`
- Enhance autoskills CLI with version display and improved technology listing `[506ad14](https://github.com/midudev/autoskills/commit/506ad14)`
- Enhance autoskills CLI with improved color handling and multi-select functionality `[b09044c](https://github.com/midudev/autoskills/commit/b09044c)`

### 📦 Other Changes

- Add LICENSE file and update project license to CC BY-NC 4.0 `[9301e31](https://github.com/midudev/autoskills/commit/9301e31)`
- Replace Tailwind skill with tailwind-css-patterns `[beffb9d](https://github.com/midudev/autoskills/commit/beffb9d)`
- Refactor CLI into modular files `[6a7c76c](https://github.com/midudev/autoskills/commit/6a7c76c)`
- Update CLI banner formatting `[aee0b13](https://github.com/midudev/autoskills/commit/aee0b13)`
- Apply oxlint fixes and oxfmt formatting across codebase `[54e69c3](https://github.com/midudev/autoskills/commit/54e69c3)`
- Remove assertion for 'skills.sh' in CLI tests `[72c193a](https://github.com/midudev/autoskills/commit/72c193a)`

## [0.1.1](https://github.com/midudev/autoskills/releases/tag/v0.1.1) (2026-03-29)

### ✨ Features

- Enhance autoskills CLI with new white color function and improved multi-select rendering `[e2c2891](https://github.com/midudev/autoskills/commit/e2c2891)`

### 📦 Other Changes

- Refactor repos to individual skills with combo detection `[52ba1bc](https://github.com/midudev/autoskills/commit/52ba1bc)`
- Update tests for skills-based API and combo detection `[5a885f4](https://github.com/midudev/autoskills/commit/5a885f4)`

## [0.1.0](https://github.com/midudev/autoskills/releases/tag/v0.1.0) (2026-03-25)

### 🎉 Initial Release

- Add autoskills CLI package `[336
```


## File: packages/autoskills/claude.ts

```
import { existsSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const SECTION_START = "<!-- autoskills:start -->";
const SECTION_END = "<!-- autoskills:end -->";

export interface CleanupResult {
  cleaned: boolean;
  deleted: boolean;
}

export function cleanupClaudeMd(projectDir: string): CleanupResult {
  const outputPath = join(projectDir, "CLAUDE.md");

  if (!existsSync(outputPath)) {
    return { cleaned: false, deleted: false };
  }

  const existing = readFileSync(outputPath, "utf-8");
  const startIdx = existing.indexOf(SECTION_START);
  const endIdx = existing.indexOf(SECTION_END);

  if (startIdx === -1 || endIdx === -1) {
    return { cleaned: false, deleted: false };
  }

  const before = existing.slice(0, startIdx);
  const after = existing.slice(endIdx + SECTION_END.length);
  const remaining = (before + after).replace(/\n{3,}/g, "\n\n").trim();

  if (!remaining || remaining === "# CLAUDE.md") {
    unlinkSync(outputPath);
    return { cleaned: true, deleted: true };
  }

  writeFileSync(outputPath, remaining + "\n");
  return { cleaned: true, deleted: false };
}

```


## File: packages/autoskills/colors.ts

```
const noColor = "NO_COLOR" in process.env;
const forceColor = "FORCE_COLOR" in process.env;
const useColor = forceColor || (!noColor && process.stdout.isTTY);

export const bold = useColor ? (s: string) => `\x1b[1m${s}\x1b[22m` : (s: string) => s;
export const dim = useColor ? (s: string) => `\x1b[2m${s}\x1b[22m` : (s: string) => s;
export const green = useColor ? (s: string) => `\x1b[32m${s}\x1b[39m` : (s: string) => s;
export const yellow = useColor ? (s: string) => `\x1b[33m${s}\x1b[39m` : (s: string) => s;
export const cyan = useColor ? (s: string) => `\x1b[36m${s}\x1b[39m` : (s: string) => s;
export const red = useColor ? (s: string) => `\x1b[31m${s}\x1b[39m` : (s: string) => s;
export const magenta = useColor ? (s: string) => `\x1b[35m${s}\x1b[39m` : (s: string) => s;
export const gray = useColor ? (s: string) => `\x1b[38;5;240m${s}\x1b[39m` : (s: string) => s;
export const white = useColor ? (s: string) => `\x1b[97m${s}\x1b[39m` : (s: string) => s;
export const pink = useColor ? (s: string) => `\x1b[38;5;218m${s}\x1b[39m` : (s: string) => s;

export const log = console.log.bind(console);
export const write = process.stdout.write.bind(process.stdout);

export const HIDE_CURSOR = process.stdout.isTTY ? "\x1b[?25l" : "";
export const SHOW_CURSOR = process.stdout.isTTY ? "\x1b[?25h" : "";
export const SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];

```


## File: packages/autoskills/installer.ts

```
import { spawn, execFileSync } from "node:child_process";
import { parseSkillPath } from "./lib.ts";
import type { SkillEntry } from "./lib.ts";
import { log, write, dim, green, cyan, red, HIDE_CURSOR, SHOW_CURSOR, SPINNER } from "./colors.ts";

export function getNpxCommand(platform: string = process.platform): string {
  return platform === "win32" ? "npx.cmd" : "npx";
}

export function getNpxSpawnOptions(platform: string = process.platform): {
  stdio: string[];
  shell: boolean;
} {
  return {
    stdio: ["pipe", "pipe", "pipe"],
    shell: platform === "win32",
  };
}

export function buildInstallArgs(skillPath: string, agents: string[] = []): string[] {
  const { repo, skillName } = parseSkillPath(skillPath);
  const args = ["-y", "skills", "add", repo];
  if (skillName) args.push("--skill", skillName);
  args.push("-y");
  if (agents.length > 0) args.push("-a", ...agents);
  return args;
}

export function buildDirectArgs(skillPath: string, agents: string[] = []): string[] {
  const { repo, skillName } = parseSkillPath(skillPath);
  const args = ["add", repo];
  if (skillName) args.push("--skill", skillName);
  args.push("-y");
  if (agents.length > 0) args.push("-a", ...agents);
  return args;
}

let _resolvedBin: string | null | undefined;

export function resolveSkillsBin(): string | null {
  if (_resolvedBin !== undefined) return _resolvedBin;
  try {
    const npx = getNpxCommand();
    execFileSync(npx, ["-y", "skills", "--version"], {
      encoding: "utf-8",
      timeout: 30_000,
      stdio: "pipe",
    });
    const whichCmd = process.platform === "win32" ? "where" : "which";
    const binPath = execFileSync(whichCmd, ["skills"], {
      encoding: "utf-8",
      timeout: 5_000,
      stdio: "pipe",
    }).trim();
    _resolvedBin = binPath || null;
  } catch {
    _resolvedBin = null;
  }
  return _resolvedBin;
}

/** @internal — exported for testing only */
export function _resetResolvedBin(): void {
  _resolvedBin = undefined;
}

interface InstallResult {
  success: boolean;
  output: string;
  stderr: string;
  exitCode: number | null;
  command: string;
}

export function installSkill(skillPath: string, agents: string[] = []): Promise<InstallResult> {
  const bin = resolveSkillsBin();

  let cmd: string;
  let args: string[];
  let opts: { stdio: string[]; shell?: boolean };
  if (bin) {
    cmd = bin;
    args = buildDirectArgs(skillPath, agents);
    opts = { stdio: ["pipe", "pipe", "pipe"] };
  } else {
    cmd = getNpxCommand();
    args = buildInstallArgs(skillPath, agents);
    opts = getNpxSpawnOptions();
  }

  const command = `${cmd} ${args.join(" ")}`;

  return new Promise((resolve) => {
    const child = spawn(cmd, args, opts as Parameters<typeof spawn>[2]);

    const stdoutChunks: Buffer[] = [];
    const stderrChunks: Buffer[] = [];
    child.stdout?.on("data", (d: Buffer) => stdoutChunks.push(d));
    child.stderr?.on("data", (d: Buffer) => stderrChunks.push(d));

    child.on("close", (code) => {
      const stdout = Buffer.concat(stdoutChunks).toString();
      const stderr = Buffer.concat(stderrChunks).toString();
      resolve({
        success: code === 0,
        output: stdout + stderr,
        stderr,
        exitCode: code,
        command,
      });
    });

    child.on("error", (err) => {
      resolve({
        success: false,
        output: err.message,
        stderr: err.message,
        exitCode: null,
        command,
      });
    });
  });
}

function sortByRepo(skills: SkillEntry[]): SkillEntry[] {
  return [...skills].sort((a, b) => {
    const repoA = parseSkillPath(a.skill).repo;
    const repoB = parseSkillPath(b.skill).repo;
    return repoA.localeCompare(repoB);
  });
}

interface InstallAllResult {
  installed: number;
  failed: number;
  errors: {
    name: string;
    output: string;
    stderr: string;
    exitCode: number | null;
    command: string;
  }[];
}

export async function installAll(
  skills: SkillEntry[],
  agents: string[] = [],
): Promise<InstallAllResult> {
  if (!process.stdout.isTTY) return installAllSimple(skills, agents);

  const CONCURRENCY = 6;
  const sorted = sortByRepo(skills);
  const total = sorted.length;

  const states = sorted.map(({ skill }) => ({
    name: skill,
    skill,
    status: "pending" as "pending" | "installing" | "success" | "failed",
    output: "",
  }));

  let frame = 0;
  let rendered = false;
  let activeCount = 0;

  function render(): void {
    if (rendered) {
      write(`\x1b[${total}A\r`);
    }
    rendered = true;
    write("\x1b[J");

    for (const state of states) {
      switch (state.status) {
        case "pending":
          write(dim(`   ◌ ${state.name}`) + "\n");
          break;
        case "installing":
          write(cyan(`   ${SPINNER[frame]}`) + ` ${state.name}...\n`);
          break;
        case "success":
          write(green(`   ✔ ${state.name}`) + "\n");
          break;
        case "failed":
          write(red(`   ✘ ${state.name}`) + dim(" — failed") + "\n");
          break;
      }
    }
  }

  write(HIDE_CURSOR);

  const timer = setInterval(() => {
    frame = (frame + 1) % SPINNER.length;
    if (activeCount > 0) render();
  }, 80);

  let installed = 0;
  let failed = 0;
  const errors: InstallAllResult["errors"] = [];
  let nextIdx = 0;

  async function worker(): Promise<void> {
    while (nextIdx < total) {
      const idx = nextIdx++;
      const state = states[idx];
      state.status = "installing";
      activeCount++;
      render();

      const result = await installSkill(state.skill, agents);

      activeCount--;
      if (result.success) {
        state.status = "success";
        installed++;
      } else {
        state.status = "failed";
        state.output = result.output;
        errors.push({
          name: state.name,
          output: result.output,
          stderr: result.stderr,
          exitCode: result.exitCode,
          command: result.command,
        });
        failed++;
      }
      render();
    }
  }

  const workers = Array.from({ length: Math.min(CONCURRENCY, total) }, () => worker());
  await Promise.all(workers);

  clearInterval(timer);
  render();
  write(SHOW_CURSOR);

  return { installed, failed, errors };
}

async function installAllSimple(
  skills: SkillEntry[],
  agents: string[] = [],
): Promise<InstallAllResult> {
  const CONCURRENCY = 6;
  const sorted = sortByRepo(skills);
  let installed = 0;
  let failed = 0;
  const errors: InstallAllResult["errors"] = [];
  let nextIdx = 0;

  async function worker(): Promise<void> {
    while (nextIdx < sorted.length) {
      const idx = nextIdx++;
      const { skill } = sorted[idx];
      const result = await installSkill(skill, agents);

      if (result.success) {
        log(green(`   ✔ ${skill}`));
        installed++;
      } else {
        log(red(`   ✘ ${skill}`) + dim(" — failed"));
        errors.push({
          name: skill,
          output: result.output,
          stderr: result.stderr,
          exitCode: result.exitCode,
          command: result.command,
        });
        failed++;
      }
    }
  }

  const workers = Array.from({ length: Math.min(CONCURRENCY, sorted.length) }, () => worker());
  await Promise.all(workers);

  return { installed, failed, errors };
}

```


## File: packages/autoskills/lib.ts

```
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";

import type { Technology, ComboSkill, ConfigFileContentBlock } from "./skills-map.ts";

export {
  SKILLS_MAP,
  COMBO_SKILLS_MAP,
  FRONTEND_PACKAGES,
  FRONTEND_BONUS_SKILLS,
  WEB_FRONTEND_EXTENSIONS,
  AGENT_FOLDER_MAP,
} from "./skills-map.ts";

export type { Technology, ComboSkill, ConfigFileContentBlock } from "./skills-map.ts";

import {
  SKILLS_MAP,
  COMBO_SKILLS_MAP,
  FRONTEND_PACKAGES,
  FRONTEND_BONUS_SKILLS,
  WEB_FRONTEND_EXTENSIONS,
  AGENT_FOLDER_MAP,
} from "./skills-map.ts";

// ── Internal Constants ───────────────────────────────────────

const AGENT_FOLDER_ENTRIES = Object.entries(AGENT_FOLDER_MAP);

const SCAN_SKIP_DIRS = new Set([
  "node_modules",
  ".git",
  "vendor",
  ".next",
  "dist",
  "build",
  ".output",
  ".nuxt",
  ".svelte-kit",
  "__pycache__",
  ".cache",
  "coverage",
  ".turbo",
  ".terraform",
  "var",
  "bin",
  "obj",
  ".vs",
]);

const GRADLE_SCAN_ROOT_FILES = [
  "build.gradle.kts",
  "build.gradle",
  "settings.gradle.kts",
  "settings.gradle",
  "gradle/libs.versions.toml",
];

const DOTNET_SCAN_ROOT_FILES = [
  "global.json",
  "NuGet.Config",
  "Directory.Build.props",
  "Directory.Packages.props",
];

// ── Gradle Scanning ──────────────────────────────────────────

export function parseSettingsGradleModules(content: string): string[] {
  const modules: string[] = [];
  const includeRe = /include\s*\(?\s*([^)]+)/g;
  let includeMatch;
  while ((includeMatch = includeRe.exec(content)) !== null) {
    const args = includeMatch[1];
    const quotedRe = /['"]([^'"]+)['"]/g;
    let quotedMatch;
    while ((quotedMatch = quotedRe.exec(args)) !== null) {
      modules.push(quotedMatch[1].replace(/^:/, "").replace(/:/g, "/"));
    }
  }
  return modules;
}

const _gradleCache = new Map<string, string[]>();

function gradleLayoutCandidatePaths(projectDir: string): string[] {
  const cached = _gradleCache.get(projectDir);
  if (cached) return cached;

  const candidates: string[] = [];
  const seen = new Set<string>();

  function add(filePath: string): void {
    if (!seen.has(filePath)) {
      candidates.push(filePath);
      seen.add(filePath);
    }
  }

  for (const f of GRADLE_SCAN_ROOT_FILES) {
    add(join(projectDir, f));
  }
  let entries: import("node:fs").Dirent[];
  try {
    entries = readdirSync(projectDir, { withFileTypes: true });
  } catch {
    entries = [];
  }
  for (const e of entries) {
    if (!e.isDirectory() || e.name.startsWith(".") || SCAN_SKIP_DIRS.has(e.name)) continue;
    for (const g of ["build.gradle.kts", "build.gradle"]) {
      add(join(projectDir, e.name, g));
    }
  }

  for (const settingsFile of ["settings.gradle.kts", "settings.gradle"]) {
    const settingsPath = join(projectDir, settingsFile);
    let content: string;
    try {
      content = readFileSync(settingsPath, "utf-8");
    } catch {
      continue;
    }
    for (const modulePath of parseSettingsGradleModules(content)) {
      for (const g of ["build.gradle.kts", "build.gradle"]) {
        add(join(projectDir, modulePath, g));
      }
    }
    break;
  }

  _gradleCache.set(projectDir, candidates);
  return candidates;
}

// ── .NET Scanning ────────────────────────────────────────────

const _dotNetCache = new Map<string, string[]>();

function dotNetLayoutCandidatePaths(projectDir: string): string[] {
  const cached = _dotNetCache.get(projectDir);
  if (cached) return cached;

  const candidates: string[] = [];
  const seen = new Set<string>();

  function add(filePath: string): void {
    if (!seen.has(filePath)) {
      candidates.push(filePath);
      seen.add(filePath);
    }
  }

  for (const f of DOTNET_SCAN_ROOT_FILES) {
    add(join(projectDir, f));
  }

  function scan(dir: string, depth: number): void {
    if (depth > 2) return;
    let entries: import("node:fs").Dirent[];
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }

    for (const e of entries) {
      if (e.isFile()) {
        const lower = e.name.toLowerCase();
        if (lower.endsWith(".sln") || lower.endsWith(".csproj") || lower.endsWith(".fsproj")) {
          add(join(dir, e.name));
        }
      } else if (e.isDirectory() && !e.name.startsWith(".") && !SCAN_SKIP_DIRS.has(e.name)) {
        scan(join(dir, e.name), depth + 1);
      }
    }
  }

  scan(projectDir, 0);

  _dotNetCache.set(projectDir, candidates);
  return candidates;
}

function resolveConfigFileContentPaths(
  projectDir: string,
  config: ConfigFileContentBlock,
): string[] {
  if (config.scanGradleLayout) {
    return gradleLayoutCandidatePaths(projectDir);
  }
  if (config.scanDotNetLayout) {
    return dotNetLayoutCandidatePaths(projectDir);
  }
  return (config.files || []).map((f) => join(projectDir, f));
}

// ── Frontend File Scanning ───────────────────────────────────

export function hasWebFrontendFiles(projectDir: string, maxDepth: number = 3): boolean {
  function scan(dir: string, depth: number): boolean {
    let entries: import("node:fs").Dirent[];
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return false;
    }

    for (const entry of entries) {
      if (entry.isFile()) {
        const name = entry.name;
        if (name.endsWith(".blade.php")) return true;

        const dot = name.lastIndexOf(".");
        if (dot !== -1 && WEB_FRONTEND_EXTENSIONS.has(name.slice(dot))) return true;
      } else if (entry.isDirectory() && depth < maxDepth) {
        if (SCAN_SKIP_DIRS.has(entry.name) || entry.name.startsWith(".")) continue;
        if (scan(join(dir, entry.name), depth + 1)) return true;
      }
    }

    return false;
  }

  return scan(projectDir, 0);
}

// ── Workspace Resolution ──────────────────────────────────────

function parsePnpmWorkspaceYaml(content: string): string[] {
  const lines = content.split("\n");
  const patterns: string[] = [];
  let inPackages = false;

  for (const raw of lines) {
    const line = raw.trim();
    if (line === "packages:" || line === "packages :") {
      inPackages = true;
      continue;
    }
    if (inPackages) {
      if (line.startsWith("- ")) {
        patterns.push(
          line
            .slice(2)
            .trim()
            .replace(/^['"]|['"]$/g, ""),
        );
      } else if (line !== "" && !line.startsWith("#")) {
        break;
      }
    }
  }

  return patterns;
}

function expandWorkspacePatterns(projectDir: string, patterns: string[]): string[] {
  const dirs: string[] = [];

  for (const pattern of patterns) {
    if (pattern.includes("*")) {
      const parent = join(projectDir, pattern.replace(/\/?\*.*$/, ""));
      let entries: import("node:fs").Dirent[];
      try {
        entries = readdirSync(parent, { withFileTypes: true });
      } catch {
        continue;
      }
      for (const entry of entries) {
        if (!entry.isDirectory() || SCAN_SKIP_DIRS.has(entry.name) || entry.name.startsWith("."))
          continue;
        const wsDir = join(parent, entry.name);
        if (
          existsSync(join(wsDir, "package.json")) ||
          existsSync(join(wsDir, "deno.json")) ||
          existsSync(join(wsDir, "deno.jsonc"))
        ) {
          dirs.push(wsDir);
        }
      }
    } else {
      const wsDir = join(projectDir, pattern);
      if (
        existsSync(join(wsDir, "package.json")) ||
        existsSync(join(wsDir, "deno.json")) ||
        existsSync(join(wsDir, "deno.jsonc"))
      ) {
        dirs.push(wsDir);
      }
    }
  }

  return dirs;
}

interface PreloadedManifests {
  pkg?: Record<string, unknown> | null;
  denoJson?: Record<string, unknown> | null;
}

export function resolveWorkspaces(projectDir: string, preloaded?: PreloadedManifests): string[] {
  const pnpmPath = join(projectDir, "pnpm-workspace.yaml");
  if (existsSync(pnpmPath)) {
    try {
      const content = readFileSync(pnpmPath, "utf-8");
      const patterns = parsePnpmWorkspaceYaml(content);
      if (patterns.length > 0) {
        return expandWorkspacePatterns(projectDir, patterns).filter(
          (d) => resolve(d) !== resolve(projectDir),
        );
      }
    } catch {}
  }

  const pkg = preloaded?.pkg !== undefined ? preloaded.pkg : readPackageJson(projectDir);
  if (pkg) {
    const ws = (pkg as Record<string, unknown>).workspaces;
    const patterns = Array.isArray(ws)
      ? (ws as string[])
      : Array.isArray((ws as Record<string, unknown>)?.packages)
        ? (ws as Record<string, string[]>).packages
        : null;
    if (patterns && patterns.length > 0) {
      return expandWorkspacePatterns(projectDir, patterns).filter(
        (d) => resolve(d) !== resolve(projectDir),
      );
    }
  }

  const denoJson =
    preloaded?.denoJson !== undefined ? preloaded.denoJson : readDenoJson(projectDir);
  if (denoJson?.workspace) {
    const members = Array.isArray(denoJson.workspace) ? (denoJson.workspace as string[]) : [];
    if (members.length > 0) {
      return expandWorkspacePatterns(projectDir, members).filter(
        (d) => resolve(d) !== resolve(projectDir),
      );
    }
  }

  return [];
}

// ── Detection ─────────────────────────────────────────────────

export function readGemfile(dir: string): string[] {
  const gemfilePath = join(dir, "Gemfile");
  if (!existsSync(gemfilePath)) return [];

  try {
    const content = readFileSync(gemfilePath, "utf-8");
    const gems: string[] = [];
    const gemRegex = /^\s*gem\s+['"]([^'"]+)['"]/gm;
    let match;
    while ((match = gemRegex.exec(content)) !== null) {
      gems.push(match[1]);
    }
    return gems;
  } catch {
    return [];
  }
}

export function readPackageJson(dir: string): Record<string, unknown> | null {
  try {
    return JSON.parse(readFileSync(join(dir, "package.json"), "utf-8"));
  } catch {
    return null;
  }
}

export function readDenoJson(dir: string): Record<string, unknown> | null {
  for (const name of ["deno.json", "deno.jsonc"]) {
    try {
      return JSON.parse(readFileSync(join(dir, name), "utf-8"));
    } catch {
      continue;
    }
  }
  return null;
}

export function getDenoImportNames(denoJson: Record<string, unknown> | null): string[] {
  if (!denoJson?.imports) return [];
  return Object.values(denoJson.imports as Record<string, string>)
    .filter((s) => typeof s === "string" && (s.startsWith("npm:") || s.startsWith("jsr:")))
    .map((specifier) => {
      const bare = specifier.replace(/^(?:npm|jsr):/, "");
      if (bare.startsWith("@")) {
        return bare.replace(/^(@[^/]+\/[^@]+).*$/, "$1");
      }
      return bare.replace(/@.*$/, "");
    });
}

export function getAllPackageNames(pkg: Record<string, unknown> | null): string[] {
  if (!pkg) return [];

  return [
    ...Object.keys((pkg.dependencies as Record<string, string>) || {}),
    ...Object.keys((pkg.devDependencies as Record<string, string>) || {}),
  ];
}

interface DetectInDirOptions {
  skipFrontendFiles?: boolean;
  pkg?: Record<string, unknown> | null;
  denoJson?: Record<string, unknown> | null;
}

interface DetectInDirResult {
  detected: Technology[];
  isFrontendByPackages: boolean;
  isFrontendByFiles: boolean;
}

function detectTechnologiesInDir(
  dir: string,
  {
    skipFrontendFiles = false,
    pkg: preloadedPkg,
    denoJson: preloadedDeno,
  }: DetectInDirOptions = {},
): DetectInDirResult {
  const pkg = preloadedPkg !== undefined ? preloadedPkg : readPackageJson(dir);
  const allPackages = getAllPackageNames(pkg);
  const deno = preloadedDeno !== undefined ? preloadedDeno : readDenoJson(dir);
  const denoImports = getDenoImportNames(deno);
  const allDepsSet =
    denoImports.length > 0 ? new Set([...allPackages, ...denoImports]) : new Set(allPackages);
  const allDepsArray = denoImports.length > 0 ? [...allDepsSet] : allPackages;
  let gemNames: string[] | undefined;
  const detected: Technology[] = [];
  const fileContentCache = new Map<string, string | null>();
  const existsCache = new Map<string, boolean>();

  function cachedRead(filePath: string): string | null {
    if (fileContentCache.has(filePath)) return fileContentCache.get(filePath)!;
    let content: string | null = null;
    try {
      content = readFileSync(filePath, "utf-8");
    } catch {}
    fileContentCache.set(filePath, content);
    if (content !== null) existsCache.set(filePath, true);
    return content;
  }

  function cachedExists(filePath: string): boolean {
    if (existsCache.has(filePath)) return existsCache.get(filePath)!;
    const result = existsSync(filePath);
    existsCache.set(filePath, result);
    return result;
  }

  for (const tech of SKILLS_MAP) {
    let found = false;

    if (tech.detect.packages) {
      found = tech.detect.packages.some((p) => allDepsSet.has(p));
    }

    if (!found && tech.detect.packagePatterns) {
      found = tech.detect.packagePatterns.some((pattern) =>
        allDepsArray.some((p) => pattern.test(p)),
      );
    }

    if (!found && tech.detect.configFiles) {
      found = tech.detect.configFiles.some((f) => cachedExists(join(dir, f)));
    }

    if (!found && tech.detect.gems) {
      if (gemNames === undefined) gemNames = readGemfile(dir);
      found = tech.detect.gems.some((g) => gemNames!.includes(g));
    }

    if (!found && tech.detect.configFileContent) {
      const configs = Array.isArray(tech.detect.configFileContent)
        ? tech.detect.configFileContent
        : [tech.detect.configFileContent];
      for (const cfg of configs) {
        const paths = resolveConfigFileContentPaths(dir, cfg);
        const { patterns } = cfg;
        for (const filePath of paths) {
          const content = cachedRead(filePath);
          if (content === null) continue;
          if (patterns.some((p) => content.includes(p))) {
            found = true;
            break;
          }
        }
        if (found) break;
      }
    }

    if (found) {
      detected.push(tech);
    }
  }

  const isFrontendByPackages = allDepsArray.some((p) => FRONTEND_PACKAGES.has(p));
  const isFrontendByFiles =
    isFrontendByPackages || skipFrontendFiles ? false : hasWebFrontendFiles(dir);

  return { detected, isFrontendByPackages, isFrontendByFiles };
}

export interface DetectResult {
  detected: Technology[];
  isFrontend: boolean;
  combos: ComboSkill[];
}

export function detectTechnologies(projectDir: string): DetectResult {
  const pkg = readPackageJson(projectDir);
  const denoJson = readDenoJson(projectDir);
  const root = detectTechnologiesInDir(projectDir, { pkg, denoJson });
  const seenIds = new Map<string, Technology>(root.detected.map((t) => [t.id, t]));
  let isFrontend = root.isFrontendByPackages || root.isFrontendByFiles;

  const workspaceDirs = resolveWorkspaces(projectDir, { pkg, denoJson });
  for (const wsDir of workspaceDirs) {
    const ws = detectTechnologiesInDir(wsDir, { skipFrontendFiles: isFrontend });

    for (const tech of ws.detected) {
      if (!seenIds.has(tech.id)) {
        seenIds.set(tech.id, tech);
      }
    }

    if (ws.isFrontendByPackages || ws.isFrontendByFiles) {
      isFrontend = true;
    }
  }

  const detected = [...seenIds.values()];
  const detectedIds = detected.map((t) => t.id);
  const combos = detectCombos(detectedIds);

  return { detected, isFrontend, combos };
}

export function detectCombos(detectedIds: string[]): ComboSkill[] {
  const idSet = detectedIds instanceof Set ? detectedIds : new Set(detectedIds);
  return COMBO_SKILLS_MAP.filter((combo) => combo.requires.every((id) => idSet.has(id)));
}

// ── Agent Detection ─────────────────────────────────────────

export function detectAgents(home: string = homedir()): string[] {
  const agents = ["universal"];

  for (const [folder, agentName] of AGENT_FOLDER_ENTRIES) {
    if (existsSync(join(home, folder, "skills"))) {
      agents.push(agentName);
    }
  }

  return agents;
}

// ── Helpers ───────────────────────────────────
```


(… 12 more files omitted due to size limit)
<!-- fetched-content:end -->
