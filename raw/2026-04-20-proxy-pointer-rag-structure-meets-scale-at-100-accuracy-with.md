---
title: "Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval | Towards Data Science"
type: url
captured: 2026-04-20T11:28:37.984414+00:00
source: android-share
url: "https://towardsdatascience.com/proxy-pointer-rag-structure-meets-scale-100-accuracy-with-smarter-retrieval/"
content_hash: "sha256:b0c679422e40d9ea2040840632aef8bb2cc822ddd3026f115ed8ff4d6db3b7a5"
tags: []
status: ingested
---

https://towardsdatascience.com/proxy-pointer-rag-structure-meets-scale-100-accuracy-with-smarter-retrieval/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-20T23:16:39+00:00
- source_url: https://towardsdatascience.com/proxy-pointer-rag-structure-meets-scale-100-accuracy-with-smarter-retrieval/
- resolved_url: https://towardsdatascience.com/proxy-pointer-rag-structure-meets-scale-100-accuracy-with-smarter-retrieval/
- content_type: text/html; charset=UTF-8
- image_urls: ["https://contributor.insightmediagroup.io/wp-content/uploads/2026/04/embedding-1024x121.png", "https://contributor.insightmediagroup.io/wp-content/uploads/2026/04/Retrieval-1024x122.png", "https://towardsdatascience.com/wp-content/uploads/2026/04/proxy-pointer-2-scaled-1.jpg", "https://towardsdatascience.com/wp-content/uploads/2026/04/proxy-pointer-2048x1143-1.jpg"]

## Fetched Content
In my
previous article
, I introduced
Proxy-Pointer RAG
— a retrieval
architecture that embeds
document structure directly into a vector index, achieving the surgical precision of “Vectorless RAG” systems like PageIndex, without their scalability and cost penalties. That article laid the foundation: the
why
, the
how
, and a promising 10-query comparison on a single World Bank report.
Although a useful proof-of-concept, that did not prove production readiness. This article aims to address that.
In an enterprise, the vast majority of documents on which RAG is applied — technical manuals, research papers, legal contracts, policy reports, annual filings, compliance documents —
have section headings.
That makes them structured. And that
structure encapsulates meaning
, precisely how a human comprehends and searches a complex document by organizing the section flow in the mind. A standard vector RAG throws away the structure, when it shreds a document into a flat bag of chunks leading to sub-optimal responses. Proxy-Pointer instead exploits that ubiquitous structure to dramatically improve retrieval accuracy, at minimal additional cost.
To stress-test the architecture, we needed the most demanding structured documents we could find — the kind where a single misplaced decimal point or a missed footnote can invalidate an entire analysis.
That’s financial filings.
10-K annual reports are deeply nested, cross-referenced across multiple financial statements, and demand precise numerical reasoning. If Proxy-Pointer can handle these, it can handle anything with headings.
This article provides evidence to support Proxy-Pointer’s capability. I took four
publicly available
FY2022 10-K filings —
AMD
(121 pages), American Express (260 pages), Boeing (190 pages), and PepsiCo (500
pages) — and tested Proxy-Pointer on
66 questions
across two distinct benchmarks, including adversarial queries specifically designed to break naive retrieval systems. The results were decisive and summarized below.
Also in this article, I’m open-sourcing the complete pipeline — so you can run it on your own documents, reproduce the results, and push it further.
## Quick Recap: What is Proxy-Pointer?
Standard vector RAG splits documents into blind chunks, embeds them, and retrieves the top-K by cosine similarity. The synthesizer LLM sees fragmented, context-less text — and frequently hallucinates or misses the answer entirely.
In the previous article, Proxy-Pointer fixed this with five zero-cost engineering techniques:
- Skeleton Tree — Parse Markdown headings into a hierarchical tree (pure Python, no LLM needed)
- Breadcrumb Injection — Prepend the full structural path ( `AMD > Financial Statements > Cash Flows` ) to every chunk before embedding
- Structure-Guided Chunking — Split text within section boundaries, never across them
- Noise Filtering — Remove distracting sections (TOC, glossary, executive summaries) from the index
- Pointer-Based Context — Use retrieved chunks as pointers to load the full, unbroken document section for the synthesizer
The result: every chunk knows
where
it lives in the document, and the synthesizer sees complete sections — not fragments.
## Refinements Since the First Article
Several significant improvements were made to the pipeline before benchmarking. These are outlined as follows:
### Indexing Pipeline Changes
Standalone Architecture.
The original implementation relied on PageIndex as a dependency for skeleton tree generation. This has been completely removed. Proxy-Pointer now ships a self-contained, ~150-line pure-Python tree builder that parses Markdown headings into a hierarchical JSON structure — zero external dependencies, zero LLM calls, runs in milliseconds.
LLM-Powered Noise Filter.
The first version used a hardcoded list of noise titles (
`NOISE_TITLES = {"contents", "foreword", ...}`
). This broke on variations like “Note of Thanks” vs. “Acknowledgments” or “
TOC
” vs. “TABLE OF CONTENTS.” In this version, the new pipeline sends the lightweight skeleton tree to
`gemini-flash-lite`
and asks it to identify noise nodes across six categories. This catches semantic equivalents that regex could not.
The updated pipeline is the following:
### Retrieval Pipeline Changes
Two-Stage Retrieval: Semantic + LLM Re-Ranker.
The first article used a simple top-K retrieval from FAISS. The refined pipeline now operates in two stages:
- Stage 1 (Broad Recall): FAISS returns the top 200 chunks by embedding similarity, which are deduplicated by `(doc_id,node_id` ) and shortlisted to 50 unique candidate nodes .
- Stage 2 (Structural Re-Ranking): The hierarchical breadcrumb paths of all 50 candidates are sent to a Gemini LLM, which re-ranks them by structural relevance — not embedding similarity — and returns the top 5. This is the key differentiator: a query about “AMD’s cash flow” now correctly prioritizes `AMD > Financial Statements > Cash Flows` over a paragraph that merely mentions cash flow.
Here is the updated pipeline:
These refinements transformed Proxy-Pointer from a promising prototype into a production-grade retrieval engine.
## Benchmarking: Two Tests, 66 Questions, Four Companies
To rigorously evaluate the pipeline, I downloaded the FY2022 10-K annual filings of
AMD
,
American Express (AMEX)
,
Boeing
, and
PepsiCo
. These were extracted to Markdown using LlamaParse and indexed through the Proxy-Pointer pipeline.
I then tested against two distinct benchmarks:
### Benchmark 1: FinanceBench (26 Questions)
FinanceBench
is an established benchmark of qualitative and quantitative questions across financial filings. I selected all 26 questions spanning the four companies in the dataset — covering numerical reasoning, information extraction and logical reasoning. Due to dataset licensing restrictions, the FinanceBench questions and ground truth answers are not included in the github repository. However, the scorecards with Proxy-Pointer responses are provided for reference.
To ensure reproducibility, the repository includes a
`benchmark.py`
script that allows you to run the full evaluation yourself on FinanceBench (or any custom dataset), generating both detailed logs and scorecards using the same pipeline.
### Benchmark 2: Comprehensive Stress Test (40 Questions)
FinanceBench, while useful, primarily tests factual recall. I needed something harder — queries that would break a system relying on surface-level chunk matching. So I created 40 custom questions, 10 per company, specifically designed to stress-test numerical reasoning, multi-hop retrieval, adversarial robustness, and cross-statement reconciliation.
The full Q&A logs using the bot and scorecards comparing with the ground truth are included in the github repository.
Here are five examples that illustrate the complexity:
Multi-hop Numerical (AMEX):
“Calculate the proportion of net interest income to total revenues net of interest expense for 2022 and compare it to 2021. Did dependence increase?”
This requires locating two different line items across two fiscal years, computing ratios for each, and then comparing them — a three-step reasoning chain that demands precise retrieval of the income statement.
Adversarial Numerical (AMD):
“Estimate whether inventory buildup contributed significantly to cash flow decline in FY2022.”
This is deliberately adversarial: it presupposes that cash flow declined (which it did, marginally) and requires the model to quantify a
balance sheet
item’s impact on a
cash flow statement
metric. A naive retriever would fetch balance sheet data but miss the cash flow context.
Reinvestment Rate (PepsiCo):
“Calculate the reinvestment rate defined as Capex divided by (Operating Cash Flow minus Dividends).”
This requires pulling three distinct figures from the cash flow statement, performing a non-standard calculation that isn’t reported anywhere in the 10-K, and arriving at a precise ratio (1.123).
Cash Flow Quality (Boeing):
“What percentage of operating cash flow in FY2022 was consumed by changes in working capital?”
The answer here is counterintuitive:
0%
— because working capital was actually a
source
of cash (+$4,139M vs. OCF of $3,512M), contributing 118% of operating cash flow. Any system that retrieves the wrong section or misinterprets the sign will fail.
Attribution (AMEX):
“Estimate how much of total revenue growth is attributable to discount revenue increase.”
This requires computing two deltas (discount revenue change and total revenue change), then expressing one as a percentage of the other — a calculation nowhere present in the filing itself.
Every question has a pre-computed ground truth answer with specific numerical values, making evaluation unambiguous.
## Results
### k=5 Configuration (Primary)
In this configuration, the retriever selects a set of 5 nodes (
`k_final = 5`
), and the corresponding sections sent to the synthesizer LLM for response.
| Benchmark | Score | Accuracy |
| --- | --- | --- |
| FinanceBench (26 questions) | 26 / 26 | 100% |
| Comprehensive (40 questions) | 40 / 40 | 100% |
| Total | 66 / 66 | 100% |
A perfect score across all 66 questions.
Every numerical value matched the ground truth. Every qualitative assessment aligned with the filing data.
To illustrate, here are two actual bot responses from the benchmark run — showing the retrieval path
and
the synthesized answer for queries cited in the previous section:
PepsiCo: Reinvestment Rate
—
“Calculate the reinvestment rate defined as Capex divided by (Operating Cash Flow minus Dividends).”
The bot retrieved
`Consolidated Statement of Cash Flows (ID: 0080)`
and
`Consolidated Statement of Cash Flows (continued) (ID: 0081)`
, then computed:
Capital spending: $5,207M / (Operating Cash Flow: $10,811M − Dividends: $6,172M) = 5,207 / 4,639 =
112.24%
(i.e., 1.1224)
Ground truth: 1.123. ✅ Match. But the bot went further — unprompted, it computed the same ratio for FY2021 (79.73%) and FY2020 (83.07%), surfacing a clear trend of accelerating reinvestment that wasn’t even asked for.
Boeing: Cash Flow Quality
—
“What percentage of operating cash flow in FY2022 was consumed by changes in working capital?”
The bot retrieved
`Boeing > Liquidity and Capital Resources > Cash Flow Summary (ID: 0082)`
and
`Consolidated Statements of Cash Flows (ID: 0107)`
, then responded:
Changes in working capital provided
$4,139M
in cash, while net operating cash flow was
$3,512M
. Because the change in working capital was a source of cash rather than a consumption, it did not consume any percentage of OCF.
Ground truth: 0% consumed; working capital was a source of cash. ✅ Match. This is a deliberately counterintuitive question — most systems would force a percentage rather than recognizing the logical inversion. The structural retrieval ensured the bot had the full cash flow statement, and the synthesizer correctly interpreted the sign.
### k=3 Configuration (Stress Test)
To understand the system’s failure boundaries, I re-ran both benchmarks with
`k_final=3`
— retrieving only 3 document sections instead of 5. This deliberately constrains the context window to test whether the retrieval precision is robust enough to work with fewer nodes.
| Benchmark | Score | Accuracy |
| --- | --- | --- |
| FinanceBench (26 questions) | 25 / 26 | 96.2% |
| Comprehensive (40 questions) | 37 / 40 | 92.5% |
| Total | 62 / 66 | 93.9% |
The failures in the k=3 run were insightful and provide more perspective than the perfect k=5 scores:
- FinanceBench: One question for AMD, suffered a calculation hallucination — the model retrieved the correct inputs ($9,981M / $6,369M) but computed the division incorrectly (outputting 1.78 instead of 1.57). The retrieval was correct; the LLM’s arithmetic was not. This is not a retrieval failure — it’s a synthesis failure, and a larger LLM (than `flash-lite` used here) likely would not have made an error.
- Comprehensive (AMEX Q7): The query “Did provisions for credit losses increase faster than total revenue?” requires both the provisions line and the total revenue line from the income statement. With k=3, the ranker prioritized the credit loss notes over the revenue summary, leaving the synthesizer without the denominator for its comparison.
- Comprehensive (AMEX Q10): Operating leverage analysis requires comparing revenue growth and expense growth side by side. At k=3, the expense breakdowns were excluded.
- Comprehensive (PepsiCo Q9): “What percentage of Russia-Ukraine charges were due to intangible asset impairments?” requires a specific footnote that, at k=3, was displaced by higher-ranking cash flow nodes.
The pattern is consistent:
every k=3 failure was caused by insufficient context coverage, not incorrect retrieval.
The ranker chose the
right
primary sections; it simply didn’t have room for the secondary ones that complex reconciliation queries demand.
This confirms an important architectural insight:
when questions require cross-referencing multiple parts of financial statements, k=5 provides the necessary coverage, while k=3 introduces retrieval gaps for the most complex reconciliations.
For most practical applications — where the majority of queries target a single section or statement — k=3 would be perfectly adequate and faster.
## What the Scorecards Don’t Show
Beyond the raw numbers, the benchmark revealed qualitative strengths worth highlighting:
Source Grounding.
Every response cited specific sources using their structural breadcrumbs (e.g.,
`AMD > Financial Condition > Liquidity and Capital Resources`
). An analyst receiving these answers can trace them directly to the filing section, creating an audit trail.
Adversarial Robustness.
When asked about crypto revenue at AMEX (which doesn’t exist), the system correctly returned “No evidence” rather than hallucinating a figure. When asked about Boeing’s Debt/Equity ratio (which is mathematically undefined due to negative equity), it explained
why
the metric is not meaningful rather than forcing a number. These are the queries that trip up systems with poor retrieval — they surface plausible-looking but irrelevant context, and the LLM invents an answer.
Outperforming Ground Truth.
In several cases, the bot’s answer was arguably
better
than our pre-computed ground truth. Boeing’s backlog change was estimated as “mid-single digit %” in the ground truth, but the bot computed the precise figure:
`+7.12%`
. AMD’s inventory impact was ground-truthed as “$1B+ drag,” but the bot identified the specific
`$1.4B buildup`
. These aren’t errors — they’re improvements made possible because the synthesizer saw the full, unedited section text, not a truncated chunk.
For detailed question-by-question results, comparison logs, and traffic-light scorecards, refer to the open source repo mentioned below.
## Open-Source Repository
Proxy-Pointer is now fully open-source (MIT License) and can be accessed at
Proxy-Pointer Github repository
.
It is designed for a
5-minute quickstart
:
```
Proxy-Pointer/
├── src/
│   ├── config.py                      # Centralized configuration
│   ├── extraction/                    # PDF → Markdown (LlamaParse)
│   ├── indexing/
│   │   ├── build_skeleton_trees.py    # Pure-Python tree builder
│   │   └── build_pp_index.py          # Noise filter + chunking + FAISS
│   └── agent/
│       ├── pp_rag_bot.py              # Interactive RAG bot
│       └── benchmark.py               # Automated benchmarking with LLM-as-a-judge
├── data/
│   ├── pdf/                           # 4 FinanceBench 10-Ks included
│   ├── documents/                     # Pre-extracted AMD Markdown (ready to index)
│   └── Benchmark/                     # Full scorecards and comparison logs
```
### What’s included out of the box
- A pre-extracted Markdown file for AMD’s FY2022 10-K — just configure your Gemini API key, build the index, and start querying in under 5 minutes.
- Three additional 10-K PDFs (AMEX, Boeing, PepsiCo) for users who want to expand their corpus.
- Scorecards for both benchmarks and full question-answer logs for 40 questions of Comprehensive benchmark.
- An automated benchmarking script with LLM-as-a-judge evaluation — bring your own Excel file with questions and ground truths, and the system generates timestamped scorecards automatically.
The entire pipeline runs on a single Gemini API key using
`gemini-flash-lite`
, the most cost effective model in Google’s lineup. No GPU required. No complex infrastructure or token-hungry and expensive indexing tree to be built.
Just clone, configure, vector index, query.
## Conclusion
When I published the first article on Proxy-Pointer, it was an interesting hypothesis: you don’t need expensive LLM-navigated trees to make retrieval structurally aware — you just need to be clever about what you embed. The evidence was a 10-query comparison on a single document.
This article moves beyond hypothesis to proof.
66 questions. Four Fortune 500 companies. 100% accuracy at k=5.
Multi-hop numerical reasoning, cross-statement reconciliation, adversarial edge cases, and counterintuitive financial metrics — Proxy-Pointer handled them all. And when we deliberately starved it of context at k=3, it still delivered 93.9% accuracy, failing only when complex queries genuinely required more than three document sections.
Here is what we achieved — and why it matters for production RAG systems:
- One architecture, all document types. Enterprises no longer need to maintain two separate retrieval pathways — Vectorless for complex, structured, high-value documents (financial filings, legal contracts, research reports) and the proven Vector RAG for routine knowledge bases. Proxy-Pointer handles both within a single, unified vector RAG pipeline. If a document has structural headings, the system exploits them. If it doesn’t, it degrades gracefully to standard chunking. No routing logic, no special cases.
- Full vector RAG scalability at the same price point. Tree-based “Vectorless” approaches require expensive LLM calls during indexing (one summary per node for all nodes in a document) and during retrieval (LLM tree navigation per query). Proxy-Pointer eliminates both. The skeleton tree is an extremely lightweight structure built with pure Python in milliseconds. Indexing uses only an embedding model — identical to standard vector RAG. The only LLM calls are the noise filter (once per document at indexing) and the re-ranker, which takes only 50 (and can even work well with half that number) breadcrumbs (tree paths) + synthesizer at query time.
- Budget-friendly models, premium results. The entire benchmark was run using `gemini-embedding-001` at half its default dimensionality (1536 instead of 3072) to optimise vector database storage and `gemini-flash-lite` — the most cost-efficient model in Google’s lineup — for noise filtering, re-ranking, and synthesis. No GPT-5, no Claude Opus, no fine-tuned models. The architecture compensates for model simplicity by delivering better context to the synthesizer.
- Transparent, auditable, explainable. Every response comes with a structural trace: which nodes were retrieved, their hierarchical breadcrumbs, and the exact line ranges in the source document. An analyst can verify any answer by opening the Markdown file and reading the cited section. This isn’t a black-box system — it’s a glass-box retrieval engine.
- Open-source and immediately usable. The complete pipeline — from PDF extraction to benchmarking — is available as a single repository with a 5-minute quickstart. Clone, configure a LLM API key, build the index and start querying. No GPU, no Docker, no complex infrastructure.
If your retrieval system is struggling with complex, structured documents, the problem is probably not your embedding model. It’s that your index has no idea where anything
lives
in the document. Give it structure, and the accuracy follows.
Clone the repo. Try your own documents. Let me know your thoughts.
Connect with me and share your comments at
www.linkedin.com/in/partha-sarkar-lets-talk-AI
All documents used in this benchmark are publicly available FY2022 10-K filings at
SEC.gov
. Code and benchmark results are open-source under the MIT License
.
Images used in this article are generated using Google Gemini.
<!-- fetched-content:end -->
