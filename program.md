# labs-wiki Research Program

> Configuration for the `/autoresearch` skill. Tune this file to shape how the
> research loop behaves. The skill reads this file before every run.

## Defaults

- **Max rounds:** 3 (discover → gather → synthesize).
- **Sources per run:** 3-5.
- **Confidence floor for filing:** ≥ 2 independent sources agree on the core claim, OR 1 primary source (arXiv paper, official spec, reference implementation).
- **Stop early if:** a wiki page on this topic exists with `last_verified` within 30 days AND `quality_score >= 70`.

## Source preference (high → low)

1. **Primary.** arXiv papers, RFCs, official language/framework specs, reference implementations, conference proceedings.
2. **Authoritative secondary.** Official documentation, whitepapers from the vendor, well-cited textbooks.
3. **Reputable secondary.** Engineering blogs from the maintainers (e.g., Anthropic, Google Research, Meta AI), well-known practitioner blogs (Simon Willison, Lilian Weng, Sebastian Raschka).
4. **Community.** Stack Overflow, GitHub discussions, reddit — only for "is this a known issue" confirmation, never as the sole citation.
5. **Tutorial/blog.** Medium, dev.to, Hashnode — only when no higher-tier source exists. Flag as `quality: blog`.

## Topics — always deep-dive (allocate max rounds)

- Core ML/LLM architecture (attention, RoPE, MoE, rotary, etc.)
- MemPalace internals, ChromaDB tuning, embedding models
- Homelab self-hosting security (auth, TLS, reverse proxy hardening)
- Real-Debrid / debrid ecosystem internals
- NBA fantasy z-score methodology, Yahoo API quirks

## Topics — skim only (1-2 rounds max)

- Generic programming language syntax
- Standard library questions
- Already-covered topics in wiki (check first, then stop)

## Topics — outside scope (refuse politely)

- Legal advice
- Medical advice
- Financial trading specifics beyond informational context

## Quality gates

A research run should **not file** a `raw/` page if:

- Fewer than 2 independent sources found.
- All sources are tutorial/blog tier (no primary or authoritative secondary).
- The user interrupted mid-round 2 and gave no "ship it anyway" signal.

In those cases, report what was found and ask the user how to proceed.

## Integration with hot cache

After a successful research run, the filed source will:

1. Be mined by `mempalace-watcher` within ~60s → searchable in the `labs_wiki` wing.
2. Be compiled by the `wiki-auto-ingest` Docker sidecar → produces wiki pages (source + referenced concepts/entities).
3. Show up in `wiki/hot.md` under "Recent Sources Captured" on the next `build_hot.py` run.

## Overrides via CLI

If the user invokes `/autoresearch <topic> --quick`, use max 2 rounds and 3 sources.
If `--deep`, max 5 rounds and 8 sources.
Default is the 3-round / 3-5 source config above.
