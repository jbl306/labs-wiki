---
title: "Node.js Installation via nvm and Global Taste-Skill Package Installation"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 59
concepts:
  - nodejs-installation-nvm-global-taste-skill-installation
related:
  - "[[Automated AI Skill Stack Installation]]"
  - "[[Custom Copilot CLI Agents]]"
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [nodejs, nvm, skill-installation, ai-agents]
---

# Node.js Installation via nvm and Global Taste-Skill Package Installation

## Overview

Sprint 12 included installing Node.js on the server using nvm (Node Version Manager) without requiring sudo privileges, enabling the use of npx to globally install a taste-skill package with multiple AI skills. This setup facilitates skill management for AI agents.

## How It Works

The server lacked Node.js and npx, preventing direct skill installation. The user installed nvm in the home directory (`~/.nvm`), which does not require sudo access, making it suitable for restricted environments.

After installing nvm, Node.js version 20.20.1 LTS was installed along with npm 10.8.2. The user must source the nvm script to activate the environment:

```bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```

With Node.js and npx available, the user ran:

```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

The installer prompted to select skills and scope; all 7 skills were installed globally to `~/.agents/skills/`. This enables AI agents to access these skills for enhanced capabilities.

An interactive prompt remains open to install an additional `find-skills` skill, indicating ongoing skill management.

## Key Properties

- **No Sudo Required:** nvm installs Node.js in user space, avoiding permission issues on shared servers.
- **Global Skill Installation:** Skills installed globally for agent access under `~/.agents/skills/`.
- **Interactive Skill Management:** Installer supports interactive prompts for skill selection and installation.

## Limitations

Requires manual sourcing of nvm environment in each shell session. Interactive prompts may block automation unless handled. Skills installed globally may require version management if multiple skill sets are used.

## Example

Installation commands:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 20
nvm use 20
npx skills add https://github.com/Leonxlnx/taste-skill
```


## Relationship to Other Concepts

- **[[Automated AI Skill Stack Installation]]** — Both involve installing AI skills for agent workflows
- **[[Custom Copilot CLI Agents]]** — Skills enhance agent capabilities in CLI environments

## Practical Applications

This method enables flexible, permission-safe installation of Node.js and AI skill packages on servers, supporting agent customization and capability extension without administrative access.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
