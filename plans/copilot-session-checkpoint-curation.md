# Copilot Session Checkpoint Curation Plan

> Created: 2026-04-18
> Scope: make Copilot checkpoint promotion align more closely with Karpathy's **LLM Wiki** pattern by keeping durable insight, reducing session-shaped clutter, and improving graph value.

---

## Goal

Keep Copilot checkpoints as a **useful compile input**, but stop treating every checkpoint as an equally valuable first-class wiki artifact.

The target outcome is:

- **durable checkpoints stay**
- **progress-log checkpoints compress upward into concepts/synthesis instead of accumulating as source clutter**
- **the graph reflects reusable knowledge, not just session provenance**
- **GitHub Models budget goes to high-signal compilation first**

---

## Why this plan exists

The current checkpoint pipeline is structurally correct, but it is only **partially** achieving the Karpathy ideal of a persistent, compounding wiki.

### Current review findings

- **52** `Copilot Session Checkpoint:*` source pages are currently in the wiki
- They are **not orphan clutter**:
  - all 52 connect into the main graph
  - average graph degree is **6.37** for checkpoint pages vs **4.5** for non-checkpoint sources
- They mostly behave as **provenance anchors**, not synthesis bridges:
  - **52/52** connect to concepts
  - **52/52** connect to entities
  - only **2/52** connect to synthesis pages
  - **0/52** directly connect to other source pages
- Quality is mixed:
  - **37/52** have `quality_score: 100`
  - **15/52** still have `quality_score: 0`

### Interpretation

This means the checkpoint promotion loop is already good at:

1. turning session outputs into graph-connected wiki nodes
2. preserving provenance
3. seeding durable concept/entity pages

But it is still weak at:

1. deciding **which checkpoints deserve first-class source pages**
2. compressing repeated implementation history into **canonical concepts**
3. promoting checkpoint material upward into **synthesis pages**
4. distinguishing **session memory** from **durable wiki knowledge**

---

## Karpathy Alignment Standard

To be considered aligned with Karpathy's LLM Wiki gist, checkpoint promotion should satisfy all of these:

1. **Compile once, reuse many**  
   The wiki should preserve insights that future sessions read instead of re-deriving.

2. **Durable over conversational**  
   The promoted unit should capture reusable architecture, decisions, failure modes, workflows, and comparisons—not just chronology.

3. **Compounding structure**  
   New material should more often strengthen concepts, entities, and synthesis pages than merely add another session-shaped source.

4. **Graph value**  
   Checkpoint-derived pages should create real topical bridges, not only provenance links.

5. **Budget discipline**  
   GitHub Models usage should prioritize checkpoint material most likely to survive long-term.

---

## Problem Breakdown

### 1. Promotion is too binary

The system currently behaves close to:

- checkpoint exists
- checkpoint passes minimum size threshold
- checkpoint becomes a wiki source page

This is too permissive. Some checkpoints are genuinely durable (architecture, debugging, design rationale). Others are mostly sprint status.

### 2. Source pages are being used as a holding area

Many checkpoint pages are useful as **evidence**, but not ideal as **canonical knowledge units**. They should often be an intermediate source that is later compressed into:

- concept pages
- entity enrichments
- synthesis pages
- workflow/runbook pages

### 3. Graph connections are mostly local, not cross-cutting

Checkpoint pages do connect well into topical clusters, but most do **not** function as bridges between clusters. This is a sign they are preserving context more than increasing the wiki's abstraction quality.

### 4. Quality controls are inconsistent

The remaining `quality_score: 0` checkpoint pages show that post-ingest normalization/scoring is incomplete, especially for backlog imports.

---

## Design Principles

### 1. Promote fewer, stronger checkpoint pages

The wiki should prefer:

- architectural inflection points
- root-cause debugging narratives
- workflow and pipeline design changes
- durable process improvements
- cross-project integration insights

The wiki should de-prioritize:

- incremental sprint progress logs
- repetitive retrain/status updates
- implementation chronology with little reusable abstraction

### 2. Split checkpoint handling into two tracks

#### Track A — Durable checkpoint source pages

Keep first-class checkpoint pages for:

- architecture/design decisions
- debugging/root-cause sessions
- pipeline changes
- graph/wiki workflow changes
- important cross-project integration work

#### Track B — Compression-first checkpoint handling

For implementation-heavy or repetitive checkpoints:

- ingest them as raw evidence
- mine concepts/entities from them
- prefer concept/entity/synthesis updates over keeping the checkpoint page prominent
- optionally archive or demote the source page after extraction

### 3. Optimize for graph compounding, not page count

Success is not "more checkpoint pages in the graph."  
Success is:

- denser lateral concept links
- more synthesis pages
- fewer low-value session-shaped sources
- better cluster bridges

### 4. Keep provenance, but demote prominence

Some checkpoint pages are worth keeping **for traceability** even when they are not ideal primary reading material. In those cases, preserve them as provenance sources while shifting user attention to:

- canonical concepts
- synthesis pages
- durable workflow docs

---

## Proposed Implementation Plan

## Phase 1 — Introduce checkpoint quality tiers

**Goal:** stop treating all checkpoints as equal.

### Changes

- Add a checkpoint classification step before export/ingest:
  - `durable-architecture`
  - `durable-debugging`
  - `durable-workflow`
  - `project-progress`
  - `low-signal`
- Use title/content heuristics first, with room for later graph-aware scoring.
- Add a frontmatter field or export metadata indicating the checkpoint class.

### Files likely touched

- `homelab/scripts/mempalace-session-curator.py`
- `labs-wiki/scripts/auto_ingest.py`
- `labs-wiki/docs/workflows.md`

### Success criteria

- backlog and future checkpoints can be filtered by signal class
- implementation/status-heavy checkpoints are identifiable before model spend

---

## Phase 2 — Separate “source retention” from “knowledge extraction”

**Goal:** let low-value checkpoints contribute knowledge without becoming prominent source clutter.

### Changes

- Add explicit retention modes:
  - **retain** → create/update checkpoint source page normally
  - **compress** → extract concepts/entities/synthesis, but minimize or later demote source page prominence
  - **skip** → keep only in raw/session memory, no wiki compile
- For `compress` checkpoints:
  - create/update concept/entity pages
  - suppress source page from `hot.md` and similar surfaced lists
  - optionally tag as archival/provenance-only

### Files likely touched

- `labs-wiki/scripts/auto_ingest.py`
- `labs-wiki/wiki/meta/hot-snapshot.md` generation path
- `labs-wiki/docs/architecture.md`
- `labs-wiki/docs/workflows.md`

### Success criteria

- checkpoint page count grows more slowly than concept/entity value
- low-signal checkpoints still inform durable pages without dominating source inventory

---

## Phase 3 — Force upward compression into synthesis

**Goal:** make checkpoint-derived knowledge compound.

### Changes

- Add checkpoint-family synthesis triggers, e.g.:
  - repeated sprint checkpoints on the same subsystem
  - repeated debugging sessions on the same failure class
  - repeated workflow changes across the same pipeline
- Generate or queue synthesis pages such as:
  - "evolution of the NBA retrain pipeline"
  - "checkpoint promotion vs MemPalace bridge patterns"
  - "graph deduplication strategies in labs-wiki"
- Prefer synthesis creation after N related checkpoints rather than more flat source pages.

### Files likely touched

- `labs-wiki/scripts/auto_ingest.py`
- `labs-wiki/scripts/watch_raw.py`
- `labs-wiki/docs/live-memory-loop.md`

### Success criteria

- checkpoint pages connect to synthesis pages more often than the current **2/52**
- repeated session history gets compressed into durable comparative documents

---

## Phase 4 — Make the graph checkpoint-aware

**Goal:** use graph position to evaluate whether checkpoint pages are paying rent.

### Changes

- Add graph health checks specific to checkpoint pages:
  - low-degree checkpoint sources
  - checkpoint pages with only provenance-style local links
  - checkpoint pages not connected to synthesis after repeated similar ingests
- Add reporting for:
  - checkpoint degree distribution
  - checkpoint → synthesis ratio
  - checkpoint community concentration
  - checkpoint pages with `quality_score: 0`
- Use these metrics to recommend:
  - merge
  - compress
  - archive
  - keep

### Files likely touched

- `labs-wiki/wiki-graph-api/graph_builder.py`
- `labs-wiki/wiki-graph-api/main.py`
- `labs-wiki/docs/architecture.md`

### Success criteria

- graph review becomes operational instead of manual
- checkpoint clutter is measurable and reducible

---

## Phase 5 — Finish backlog cleanup and quality normalization

**Goal:** bring the already-ingested checkpoint corpus up to the new standard.

### Changes

- Review the existing 52 checkpoint pages and classify each into:
  - keep
  - compress
  - archive/provenance-only
- Re-run quality normalization for zero-score pages
- Create a focused backlog for:
  - highest-value architecture/debugging checkpoints to preserve
  - sprint/progress checkpoints to compress or demote

### Files likely touched

- `labs-wiki/wiki/sources/copilot-session-checkpoint-*.md`
- `labs-wiki/wiki/concepts/*.md`
- `labs-wiki/wiki/synthesis/*.md`
- `labs-wiki/wiki/log.md`

### Success criteria

- all retained checkpoint pages have valid quality scoring
- most low-signal checkpoint material is represented in concepts/synthesis instead of only source pages

---

## Recommended Prioritization

### Keep first

- `Copilot Session Checkpoint: Session Wiki Promotion`
- `Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup`
- `Copilot Session Checkpoint: GitHub Crawling and Richer Extraction`
- `Copilot Session Checkpoint: Fixing MemPalace Timeouts`

These are the closest to Karpathy-aligned durable knowledge because they encode architecture, workflow, graph structure, and debugging patterns.

### Compress aggressively

- repetitive sprint progress checkpoints
- retrain/status checkpoints that mostly differ by chronology
- implementation updates that already have strong concept/entity extraction

### Keep as provenance, not as primary knowledge

- checkpoints that are useful for auditability or root-cause traceability but not ideal as canonical reading pages

---

## Metrics to Track

### Quality metrics

- checkpoint pages with `quality_score: 0`
- average checkpoint degree
- checkpoint pages with synthesis neighbors
- checkpoint pages classified as durable vs progress vs low-signal

### Karpathy-alignment metrics

- ratio of checkpoint ingests that create/update synthesis pages
- ratio of checkpoint ingests that create durable concepts/entities without retaining a prominent source page
- checkpoint page growth vs concept/synthesis growth
- repeat-question answers satisfied from canonical pages instead of checkpoint sources

---

## Decision Rule

Going forward, the default policy should be:

1. **Promote checkpoint raw summaries, not transcripts**
2. **Retain only the checkpoint pages that preserve durable insight**
3. **Compress the rest into concept/entity/synthesis pages**
4. **Measure graph value, not just ingest success**

This keeps the current checkpoint system, but makes it serve the wiki instead of slowly turning the wiki into a session archive.
