# Quality Evaluation: April 10, 2026 Ingests

**Date evaluated:** 2026-04-10
**Sources reviewed:** 5 raw captures → 29 wiki pages generated
**Method:** Compared every generated wiki page against original source material (arXiv abstracts, GitHub READMEs)

---

## Executive Summary

The auto-ingest pipeline produces **structurally sound pages** with **consistently complete frontmatter** and **generally accurate content**. The main systemic issues are: broken wikilinks to pages that were never created, thin entity pages that feel template-generated, and quality_score/tier never being populated beyond defaults (0/hot). For arXiv papers where the pipeline only has access to the PDF URL (not full text), content quality is surprisingly good — the LLM is clearly extracting meaningful concepts. For GitHub repos, extraction is thorough.

### Scorecard

| Source | Pages | Accuracy | Completeness | Cross-refs | Depth | Overall |
|--------|:-----:|:--------:|:------------:|:----------:|:-----:|:-------:|
| Lottery Ticket Hypothesis (1803.03635) | 6 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **A** |
| Recursive Language Models (2512.24601) | 3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | **B+** |
| LLM Reasoning Failures (2602.06176) | 6 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | **B+** |
| AXI: Agent eXperience Interface | 7 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **B** |
| AutoSkills (midudev) | 7 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | **B** |

---

## Per-Source Evaluation

### 1. Lottery Ticket Hypothesis (arXiv 1803.03635) — Grade: A

**Pages generated:** source + 3 concepts (lottery-ticket-hypothesis, iterative-pruning-technique, initialization-sensitivity) + 2 entities (Jonathan Frankle, Michael Carlin)

**Strengths:**
- Mathematical notation is correct (⊙ elementwise product, ‖m‖₀ notation)
- Specific experimental results cited accurately (9.2% of original size, 3.5x faster)
- Concept decomposition is excellent — 3 distinct, non-overlapping concepts extracted
- Source page correctly identifies authors, date (2019-04-07), and arXiv URL
- Strong wikilink density between all generated pages

**Weaknesses:**
- Entity pages mark "Created" and "Creator" as "Unknown" — should inherit from paper metadata
- Frankle ↔ Carbin lack reciprocal entity links to each other
- All pages have `quality_score: 0` (not auto-populated)

**Verdict:** Best ingest of the batch. The pipeline excels at papers with clear, decomposable concepts.

---

### 2. Recursive Language Models (arXiv 2512.24601) — Grade: B+

**Pages generated:** source + 1 concept (recursive-language-models) + 1 entity (RLM-Qwen3-8B)

**Ground truth (from abstract):** RLMs treat long prompts as external environment, enable recursive self-invocation, process inputs 2 orders of magnitude beyond context window, RLM-Qwen3-8B outperforms base Qwen3-8B by 28.3% and approaches GPT-5 quality.

**Strengths:**
- Core claims are accurately captured: recursive paradigm, 10M+ token scale, 28.3% improvement
- Concept page includes pseudocode algorithm — impressive depth
- Correctly identifies authors (Alex Zhang, Tim Kraska, Omar Khattab) and GitHub repo link
- Good contextual links to [[Context Compaction]], [[RAG]], [[Code Generation Agents]]

**Weaknesses:**
- Only 3 pages generated (vs 6 for Lottery Ticket) — fewer concepts extracted
- Entity page has duplicate `[[Recursive Language Models]]` in related section (copy-paste bug)
- Source page has self-referential wikilink (links to itself)
- Missing GPT-5 entity page despite being a key comparison point (one exists but from another source)

**Verdict:** Accurate but less thorough concept decomposition than the Lottery Ticket ingest.

---

### 3. LLM Reasoning Failures Survey (arXiv 2602.06176) — Grade: B+

**Pages generated:** source + 3 concepts (taxonomy-of-llm-reasoning-failures, cognitive-biases-in-llms, theory-of-mind-in-llms) + 1 entity (awesome-llm-reasoning-failures-repository) + 1 synthesis (comparing-reasoning-failures-in-llms-and-human-cognitive-biases)

**Ground truth (from abstract):** Comprehensive survey of reasoning failures, two-axis taxonomy (reasoning type × failure type), covers embodied vs non-embodied reasoning, formal vs informal reasoning.

**Strengths:**
- Taxonomy accurately captured with both axes
- Generated a **synthesis page** — the only ingest to produce one (comparing LLM failures to human cognitive biases)
- Good concept decomposition: taxonomy, cognitive biases, theory of mind
- Specific examples included (Sally-Anne false-belief test)
- Detects and creates entity for the companion GitHub "Awesome" repository

**Weaknesses:**
- **Date error:** Paper dated 2026-02-05 in wiki; arXiv shows submission Dec 2025 (v1), revision Jan 2026 (v2)
- **Broken wikilink:** `[[Human Cognitive Biases]]` referenced in synthesis page but page doesn't exist
- Synthesis page cites an external GeeksforGeeks source not in `raw/` — provenance violation
- Incomplete author attribution (only lists Song, Han, Goodman — paper likely has more authors)

**Verdict:** Most ambitious ingest (produced synthesis page), but also the most broken links. The synthesis page's external source citation is a provenance concern.

---

### 4. AXI: Agent eXperience Interface (github.com/kunchenguid/axi) — Grade: B

**Pages generated:** source + 2 concepts (axi-design-principles, toon-format) + 4 entities (AXI, TOON, gh-axi, chrome-devtools-axi)

**Ground truth (from README):** 10 design principles for agent-ergonomic CLIs, TOON format (~40% token savings over JSON), benchmark results (100% success rate, lower cost/turns vs MCP), two reference implementations (gh-axi, chrome-devtools-axi).

**Strengths:**
- All 10 principles correctly enumerated with accurate descriptions
- TOON format well-explained with format examples
- Benchmark claims captured (though not deeply analyzed)
- Correctly identifies two reference implementations as separate entities
- Source page captures notable quotes from README

**Weaknesses:**
- **2 broken wikilinks** in AXI Design Principles: `[[Agent Handoffs in VS Code]]`, `[[The Context Hygiene Principle]]` — pages don't exist
- TOON entity has `Creator: Unknown` despite Kun Chen being documented as AXI creator
- TOON entity links to `https://toonformat.dev/` — this URL is from the README but appears to be a placeholder
- Entity pages are thin skeletons (50-52 lines) — "No related entities documented yet" on all four
- `Created: 2026` on AXI entity — the repo README doesn't specify a creation date, so this appears fabricated
- Benchmark data (the strongest part of the README) is only briefly mentioned, not deeply captured

**Verdict:** Good concept extraction but entity pages lack substance. Benchmark data — arguably the most valuable part of this source — deserved its own concept page.

---

### 5. AutoSkills (github.com/midudev/autoskills) — Grade: B

**Pages generated:** source + 3 concepts (automated-skill-installation, supply-chain-security-hardening, claude-code-skill-summarization) + 3 entities (AutoSkills, skills.sh, Claude Code)

**Ground truth (from README):** `npx autoskills` scans project → detects tech stack → installs skills from skills.sh, generates CLAUDE.md for Claude Code, supports wide tech stack, requires Node.js >= 22, CC BY-NC 4.0 license.

**Strengths:**
- **Most thorough extraction of the batch** — the supply chain security concept was extracted from the repo's AGENTS.md, not just the README
- Specific CLI commands, flags, and file paths accurately captured
- Correct identification of pnpm toolchain specifics (lockfile, frozen-lockfile)
- Good decomposition: automated installation, supply chain security, skill summarization are three distinct useful concepts
- Entity pages correctly attribute creator as "midudev"

**Weaknesses:**
- **4 broken wikilinks** across concept pages: `[[Skill Design Framework for AI Agents]]`, `[[Supply Chain Security]]`, `[[Claude Code Principles]]`, `[[Deterministic Installs]]`
- Inconsistent link naming: references `[[Supply Chain Security]]` when the actual page is `[[Supply Chain Security Hardening for AI Agent Projects]]`
- Claude Code entity has `Creator: Unknown` — should be Anthropic
- skills.sh entity has `Creator: Unknown` — understandable since README doesn't specify
- Date inconsistency: frontmatter says 2026-04-10, entity table says "2025"

**Verdict:** Deepest extraction (pulled from AGENTS.md beyond just README), but most broken cross-references. The pipeline creates wikilinks to "aspirational" pages that it doesn't actually generate.

---

## Systemic Issues (Cross-Source)

### 🔴 Critical: Broken Wikilinks

**8+ broken wikilinks** across today's ingests. The pipeline creates `[[wikilinks]]` to pages it thinks *should* exist but doesn't create them. This is the #1 quality issue.

| Source | Broken Links |
|--------|-------------|
| LLM Reasoning Failures | `[[Human Cognitive Biases]]` |
| AXI | `[[Agent Handoffs in VS Code]]`, `[[The Context Hygiene Principle]]` |
| AutoSkills | `[[Skill Design Framework for AI Agents]]`, `[[Supply Chain Security]]`, `[[Claude Code Principles]]`, `[[Deterministic Installs]]` |

**Root cause:** The LLM generates `related:` wikilinks to conceptually related topics without checking if those pages exist. The template/prompt needs a constraint: "only link to pages you are creating in this ingest batch."

### 🟡 Medium: Entity Pages Are Thin

Entity pages follow a rigid template producing 50-52 line skeletons. They lack:
- Reciprocal entity links (Frankle ↔ Carbin, AXI ↔ gh-axi ↔ chrome-devtools-axi)
- "Created" and "Creator" fields often say "Unknown" even when derivable
- No entity-specific context beyond what's in the source page

**Root cause:** Entity template is too minimal. The extraction prompt should push for richer entity facts.

### 🟡 Medium: quality_score and tier Never Populated

Every single page has `quality_score: 0` and `tier: hot`. These fields exist in the schema but are never calculated.

**Root cause:** The auto-ingest pipeline generates pages but doesn't run the quality scoring logic afterward. This should be a post-ingest step.

### 🟡 Medium: Self-Referential and Duplicate Wikilinks

- RLM source page links to `[[Recursive Language Models]]` (itself)
- RLM entity page has `[[Recursive Language Models]]` listed twice in `related:`
- These are minor but indicate the deduplication/self-reference check is missing

### 🟠 Low: Date Fabrication

- AXI entity: `Created: 2026` — fabricated (repo doesn't specify)
- LLM Reasoning: Paper dated `2026-02-05` — should be late 2025 (v1 submission)
- The pipeline sometimes invents dates or rounds to the ingest date

### 🟠 Low: Provenance Violations

- LLM Reasoning synthesis page cites GeeksforGeeks — an external source not in `raw/`
- Every fact should trace to a `sources:` entry per AGENTS.md rules

---

## Recommendations

### Immediate Fixes (Auto-Ingest Pipeline)

1. **Constrain wikilinks** — Only generate `[[links]]` to pages being created in the same ingest batch, OR to pages confirmed to exist in `wiki/index.md`
2. **Add reciprocal entity links** — When creating multiple entities from the same source, link them to each other
3. **Remove self-references** — Filter out wikilinks that point to the page itself
4. **Deduplicate related entries** — Check for duplicates before writing `related:` field

### Pipeline Enhancements

5. **Post-ingest quality scoring** — Run lint/scoring after page generation to populate `quality_score`
6. **Richer entity extraction** — Expand entity template to extract more facts (creator, creation date, relationships)
7. **Date validation** — Don't fabricate creation dates; use "Unknown" if not derivable
8. **Provenance enforcement** — Reject claims that can't trace to the raw source

### Benchmark Pages (Missing Value)

9. **AXI benchmarks** deserved a dedicated concept page — the quantitative comparison data (490 runs, cost/accuracy/latency) is the most valuable part of that source
10. Consider a "benchmark" or "evaluation" page type for quantitative results

---

## Raw Data

| Raw Source | File | Status | Pages | Log Entry |
|-----------|------|--------|:-----:|:---------:|
| Lottery Ticket Hypothesis | `raw/2026-04-10-180303635v5pdf.md` | ingested | 6 | ✅ |
| Recursive Language Models | `raw/2026-04-10-251224601v2pdf.md` | ingested | 3 | ✅ |
| LLM Reasoning Failures | `raw/2026-04-10-260206176v1pdf.md` | ingested | 6 | ✅ |
| AXI Repository | `raw/2026-04-10-httpsgithubcomkunchenguidaxi.md` | ingested | 7 | ✅ |
| AutoSkills Repository | `raw/2026-04-10-httpsgithubcommidudevautoskills.md` | ingested | 7 | ✅ |

**Total: 5 sources → 29 wiki pages (avg 5.8 pages/source)**
