# Wiki Audit Log

> Structured log of all wiki operations. Each entry is a YAML block.
> Appended by `/wiki-ingest`, `/wiki-update`, `/wiki-lint`, `/wiki-orchestrate`.

```yaml
- timestamp: 2026-04-07T04:00:00Z
  operation: setup
  agent: system
  targets:
    - wiki/index.md
    - wiki/log.md
  source: initial-setup
  status: success
  notes: "Wiki initialized — directory structure, schema, skills, scripts, docs, and ingest API created."

- timestamp: 2026-04-07T18:17:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/llm-wiki.md
    - wiki/concepts/llm-wiki.md
    - wiki/concepts/schema-for-llm-wiki.md
    - wiki/concepts/ingest-operation-llm-wiki.md
    - wiki/concepts/query-operation-llm-wiki.md
    - wiki/concepts/lint-operation-llm-wiki.md
    - wiki/entities/obsidian.md
    - wiki/entities/qmd.md
    - wiki/entities/vannevar-bush.md
    - wiki/entities/memex.md
  source: raw/2026-04-07-llm-wiki.md
  status: success
  notes: "Auto-ingested 10 pages (5 concepts, 4 entities)"

- timestamp: 2026-04-07T18:20:13+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/transformer-architecture-note.md
    - wiki/concepts/transformer-architecture.md
    - wiki/concepts/self-attention-mechanism.md
    - wiki/concepts/multi-head-attention.md
    - wiki/concepts/positional-encoding.md
    - wiki/entities/attention-is-all-you-need.md
  source: raw/2026-04-07-transformer-architecture-note.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities)"

- timestamp: 2026-04-07T19:52:47+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/htmx-html-over-the-wire.md
    - wiki/concepts/html-over-the-wire.md
    - wiki/entities/htmx.md
    - wiki/entities/intercooler-js.md
  source: raw/2026-04-07-test-github-repo.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities)"

- timestamp: 2026-04-07T19:52:49+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/test-tweet-with-image.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 1 pages (0 concepts, 0 entities)"

- timestamp: 2026-04-07T19:54:17+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system.md
    - wiki/entities/andrej-karpathy.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities)"

- timestamp: 2026-04-07T19:55:23+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system.md
    - wiki/entities/andrej-karpathy.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities)"

- timestamp: 2026-04-07T19:57:16+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system.md
    - wiki/concepts/embedding-based-filesystem.md
    - wiki/concepts/context-window.md
    - wiki/entities/llm-os.md
    - wiki/entities/openai-gpt-4-turbo.md
    - wiki/entities/ada002.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities)"

- timestamp: 2026-04-07T23:03:46+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/custom-agents-in-vs-code.md
    - wiki/concepts/custom-agent.md
    - wiki/concepts/handoffs.md
    - wiki/concepts/agent-file-structure.md
    - wiki/concepts/agent-skills.md
    - wiki/concepts/subagents.md
    - wiki/concepts/hooks.md
    - wiki/entities/visual-studio-code.md
    - wiki/entities/github-copilot.md
  source: raw/2026-04-07-custom-agents-in-vs-code.md
  status: success
  notes: "Auto-ingested 9 pages (6 concepts, 2 entities)"

- timestamp: 2026-04-07T23:17:13+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/jbl306homelab.md
    - wiki/concepts/homelab.md
    - wiki/entities/jbl306.md
  source: raw/2026-04-07-jbl306homelab.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities)"

- timestamp: 2026-04-07T23:30:04+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/jbl306homelab.md
    - wiki/concepts/homelab-infrastructure.md
    - wiki/concepts/cloudflare-tunnel.md
    - wiki/concepts/adguard-dns-rewrites.md
    - wiki/concepts/resource-limits-docker.md
    - wiki/concepts/automated-deployment-github-actions.md
    - wiki/concepts/service-monitoring-notifications.md
    - wiki/concepts/tailscale-vpn-setup.md
    - wiki/concepts/riven-vfs-fuse-mount.md
    - wiki/entities/beelink-gti13-ultra.md
    - wiki/entities/cloudflare-tunnel-entity.md
    - wiki/entities/caddy.md
    - wiki/entities/adguard-home.md
    - wiki/entities/tailscale.md
    - wiki/entities/riven.md
    - wiki/entities/uptime-kuma.md
    - wiki/entities/grafana.md
    - wiki/entities/ntfy.md
  source: raw/2026-04-07-jbl306homelab.md
  status: success
  notes: "Auto-ingested 18 pages (8 concepts, 9 entities)"

- timestamp: 2026-04-08T00:43:50+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/top-15-machine-learning-algorithms-every-data-scientist-should-know-in-2025.md
    - wiki/concepts/machine-learning-algorithm.md
    - wiki/concepts/supervised-learning.md
    - wiki/concepts/unsupervised-learning.md
    - wiki/concepts/reinforcement-learning.md
    - wiki/concepts/semi-supervised-learning.md
    - wiki/concepts/linear-regression.md
    - wiki/concepts/logistic-regression.md
    - wiki/concepts/decision-trees.md
    - wiki/concepts/k-nearest-neighbours.md
    - wiki/concepts/naive-bayes-classifier.md
    - wiki/concepts/k-means-clustering.md
    - wiki/concepts/support-vector-machine.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/concepts/random-forests.md
    - wiki/concepts/artificial-neural-networks.md
    - wiki/concepts/principal-component-analysis.md
    - wiki/concepts/adaboost-adaptive-boosting.md
    - wiki/concepts/long-short-term-memory-networks.md
    - wiki/concepts/lightgbm.md
    - wiki/concepts/xgboost.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
  status: success
  notes: "Auto-ingested 22 pages (20 concepts, 1 entities)"

- timestamp: 2026-04-08T01:04:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/top-15-machine-learning-algorithms-every-data-scientist-should-know-in-2025.md
    - wiki/concepts/linear-regression-algorithm.md
    - wiki/concepts/logistic-regression-algorithm.md
    - wiki/concepts/decision-trees-algorithm.md
    - wiki/concepts/k-nearest-neighbours-algorithm.md
    - wiki/concepts/naive-bayes-classifier-algorithm.md
    - wiki/concepts/k-means-clustering-algorithm.md
    - wiki/concepts/support-vector-machine-algorithm.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/concepts/random-forests-algorithm.md
    - wiki/concepts/artificial-neural-networks-algorithm-ann.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
  status: success
  notes: "Auto-ingested 12 pages (10 concepts, 1 entities)"

- timestamp: 2026-04-08T01:10:49+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/linear-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/linear-regression-algorithm.md
    - wiki/concepts/least-squares-method.md
    - wiki/concepts/gradient-descent.md
    - wiki/concepts/mean-squared-error.md
    - wiki/concepts/assumptions-of-linear-regression.md
    - wiki/concepts/regularization-techniques-linear-models.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 8 pages (6 concepts, 1 entities)"

- timestamp: 2026-04-08T01:11:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/logistic-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/logistic-regression-algorithm.md
    - wiki/concepts/sigmoid-function.md
    - wiki/concepts/softmax-function.md
    - wiki/concepts/maximum-likelihood-estimation-logistic-regression.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities)"

- timestamp: 2026-04-08T01:12:32+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/decision-tree-geeksforgeeks.md
    - wiki/concepts/decision-tree-structure.md
    - wiki/concepts/splitting-criteria-decision-trees.md
    - wiki/concepts/pruning-in-decision-trees.md
    - wiki/concepts/types-of-decision-trees.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-decision-tree-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities)"

- timestamp: 2026-04-08T01:12:51+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/k-nearest-neighborknn-algorithm-geeksforgeeks.md
    - wiki/concepts/k-nearest-neighbours-algorithm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-k-nearest-neighborknn-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities)"

- timestamp: 2026-04-08T01:14:06+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/naive-bayes-classifiers-geeksforgeeks.md
    - wiki/concepts/naive-bayes-classifier-algorithm.md
    - wiki/concepts/bayes-theorem.md
    - wiki/concepts/gaussian-naive-bayes.md
    - wiki/concepts/multinomial-naive-bayes.md
    - wiki/concepts/bernoulli-naive-bayes.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 7 pages (5 concepts, 1 entities)"

- timestamp: 2026-04-08T01:14:17+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/apriori-algorithm-geeksforgeeks.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/concepts/association-rule-metrics.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-apriori-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities)"

- timestamp: 2026-04-08T01:14:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/support-vector-machine-svm-algorithm-geeksforgeeks.md
    - wiki/concepts/support-vector-machine-algorithm.md
    - wiki/concepts/kernel-trick.md
    - wiki/concepts/hinge-loss.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-support-vector-machine-svm-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities)"

- timestamp: 2026-04-08T01:14:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/random-forest-regression-in-python-geeksforgeeks.md
    - wiki/concepts/random-forest-regression.md
    - wiki/concepts/bagging-bootstrap-aggregating.md
    - wiki/entities/randomforestregressor.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-random-forest-regression-in-python-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (2 concepts, 2 entities)"

- timestamp: 2026-04-08T01:18:42+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/implementing-the-adaboost-algorithm-from-scratch-geeksforgeeks.md
    - wiki/concepts/adaboost-algorithm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-implementing-the-adaboost-algorithm-from-scratch-geeksforgee.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities)"

- timestamp: 2026-04-08T01:18:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/artificial-neural-networks-and-its-applications-geeksforgeeks.md
    - wiki/concepts/artificial-neural-networks-architecture.md
    - wiki/concepts/artificial-neurons-vs-biological-neurons.md
    - wiki/concepts/activation-functions-in-neural-networks.md
    - wiki/concepts/types-of-artificial-neural-networks.md
    - wiki/concepts/optimization-algorithms-in-ann-training.md
    - wiki/concepts/applications-of-artificial-neural-networks.md
    - wiki/concepts/challenges-in-artificial-neural-networks.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-artificial-neural-networks-and-its-applications-geeksforgeek.md
  status: success
  notes: "Auto-ingested 9 pages (7 concepts, 1 entities)"

- timestamp: 2026-04-08T01:19:33+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/principal-component-analysis-pca-geeksforgeeks.md
    - wiki/concepts/principal-component-analysis-pca.md
    - wiki/concepts/covariance-matrix.md
    - wiki/concepts/eigenvectors-eigenvalues.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-principal-component-analysis-pca-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities)"

- timestamp: 2026-04-08T01:19:33+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/what-is-lstm-long-short-term-memory-geeksforgeeks.md
    - wiki/concepts/long-short-term-memory-lstm.md
    - wiki/concepts/forget-gate-lstm.md
    - wiki/concepts/input-gate-lstm.md
    - wiki/concepts/output-gate-lstm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-what-is-lstm-long-short-term-memory-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities)"

- timestamp: 2026-04-08T01:20:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
    - wiki/concepts/lightgbm-framework.md
    - wiki/concepts/lightgbm-core-parameters.md
    - wiki/concepts/lightgbm-boosting-algorithms.md
    - wiki/concepts/lightgbm-feature-importance-visualization.md
    - wiki/concepts/lightgbm-parallel-gpu-training.md
    - wiki/entities/lightgbm.md
    - wiki/entities/microsoft.md
    - wiki/entities/shap-shapley-additive-explanations.md
  source: raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 9 pages (5 concepts, 3 entities)"

- timestamp: 2026-04-08T01:20:15+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introduction-to-recurrent-neural-networks-geeksforgeeks.md
    - wiki/concepts/recurrent-neural-networks-rnns.md
    - wiki/concepts/backpropagation-through-time-bptt.md
    - wiki/concepts/variants-of-recurrent-neural-networks.md
    - wiki/concepts/types-of-recurrent-neural-networks.md
    - wiki/concepts/vanishing-exploding-gradient-problems-rnns.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-introduction-to-recurrent-neural-networks-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 7 pages (5 concepts, 1 entities)"

- timestamp: 2026-04-08T01:21:55+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/tracing-the-thoughts-of-a-large-language-model.md
    - wiki/concepts/ai-microscope-language-model-interpretability.md
    - wiki/concepts/conceptual-universality-multilingual-models.md
    - wiki/concepts/planning-parallel-reasoning-language-models.md
    - wiki/concepts/faithful-unfaithful-reasoning-language-models.md
    - wiki/concepts/hallucination-refusal-mechanisms-language-models.md
    - wiki/concepts/jailbreaks-safety-mechanisms-language-models.md
    - wiki/entities/anthropic.md
    - wiki/entities/claude.md
  source: raw/2026-04-08-httpswwwanthropiccomresearchtracing-thoughts-language-model.md
  status: success
  notes: "Auto-ingested 9 pages (6 concepts, 2 entities)"

- timestamp: 2026-04-08T01:21:58+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning.md
    - wiki/concepts/nested-learning-paradigm.md
    - wiki/concepts/hope-architecture.md
    - wiki/concepts/continuum-memory-system.md
    - wiki/entities/hope.md
    - wiki/entities/titans-architecture.md
  source: raw/2026-04-08-httpsresearchgoogleblogintroducing-nested-learning-a-new-ml-.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities)"

- timestamp: 2026-04-08T01:22:08+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/vision-language-action-vla-models-concepts-progress-applications-and-challenges.md
    - wiki/concepts/vision-language-action-vla-models.md
    - wiki/concepts/multimodal-alignment-vla-models.md
    - wiki/concepts/benchmark-datasets-vla-models.md
    - wiki/entities/ai2-thor.md
    - wiki/entities/habitat.md
  source: raw/2026-04-08-httpsarxivorgpdf250504769.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities)"

- timestamp: 2026-04-08T01:31:11+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/vision-language-action-vla-models-concepts-progress-applications-and-challenges.md
    - wiki/concepts/vision-language-action-vla-models.md
    - wiki/concepts/multimodal-integration-vla-models.md
    - wiki/concepts/tokenization-representation-vla-models.md
    - wiki/entities/robotic-transformer-2-rt-2.md
    - wiki/entities/cliport.md
    - wiki/entities/vima.md
  source: raw/2026-04-08-httpsarxivorgpdf250504769.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities)"

- timestamp: 2026-04-08T01:36:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-hardening-principle-10-claude-code-principles.md
    - wiki/concepts/the-hardening-principle.md
    - wiki/entities/claude.md
    - wiki/entities/obsidian.md
    - wiki/entities/ffmpeg.md
    - wiki/entities/whisper.md
  source: raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 4 entities)"

- timestamp: 2026-04-08T01:36:35+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/10-claude-code-principles-what-the-research-actually-says.md
    - wiki/concepts/the-hardening-principle.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/concepts/the-living-documentation-principle.md
    - wiki/concepts/the-disposable-blueprint-principle.md
    - wiki/concepts/the-institutional-memory-principle.md
    - wiki/concepts/the-specialized-review-principle.md
    - wiki/concepts/the-observability-imperative.md
    - wiki/concepts/the-strategic-human-gate-principle.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/concepts/the-toolkit-principle.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
    - wiki/entities/metagpt.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/prism-persona-research-framework.md
  source: raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
  status: success
  notes: "Auto-ingested 16 pages (10 concepts, 5 entities)"

- timestamp: 2026-04-08T01:36:36+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-context-hygiene-principle-10-claude-code-principles.md
    - wiki/concepts/context-hygiene-principle.md
    - wiki/concepts/u-shaped-attention-curve.md
    - wiki/concepts/progressive-disclosure-context-loading.md
    - wiki/concepts/context-poisoning.md
    - wiki/entities/claude.md
    - wiki/entities/anthropic.md
    - wiki/entities/rotary-position-embedding.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities)"

- timestamp: 2026-04-08T01:36:47+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-living-documentation-principle-10-claude-code-principles.md
    - wiki/concepts/living-documentation-principle.md
    - wiki/concepts/documentation-freshness-ci-pipeline.md
    - wiki/concepts/few-shot-context-documentation.md
    - wiki/concepts/structured-documentation-formats.md
    - wiki/concepts/architecture-decision-records-adrs.md
    - wiki/entities/claude-code.md
  source: raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (5 concepts, 1 entities)"

- timestamp: 2026-04-08T01:36:52+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-disposable-blueprint-principle-10-claude-code-principles.md
    - wiki/concepts/the-disposable-blueprint-principle.md
    - wiki/entities/metagpt-framework.md
    - wiki/entities/claude.md
    - wiki/entities/anthropic.md
  source: raw/2026-04-08-the-disposable-blueprint-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities)"

- timestamp: 2026-04-08T01:37:04+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-institutional-memory-principle-10-claude-code-principles.md
    - wiki/concepts/the-institutional-memory-principle.md
    - wiki/entities/chi-2023-why-johnny-cant-prompt.md
    - wiki/entities/anthropic-skill-creator-documentation.md
    - wiki/entities/mast-failure-taxonomy.md
  source: raw/2026-04-08-the-institutional-memory-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities)"

- timestamp: 2026-04-08T01:37:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-observability-imperative-10-claude-code-principles.md
    - wiki/concepts/the-observability-imperative.md
    - wiki/concepts/mast-failure-taxonomy.md
    - wiki/concepts/structured-artifact-approach.md
    - wiki/entities/metagpt.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/anthropic-building-effective-agents-guide.md
  source: raw/2026-04-08-the-observability-imperative-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities)"

- timestamp: 2026-04-08T01:37:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-specialized-review-principle-10-claude-code-principles.md
    - wiki/concepts/the-specialized-review-principle.md
    - wiki/concepts/vocabulary-routing-embedding-space.md
    - wiki/concepts/prism-persona-science.md
    - wiki/concepts/rubber-stamp-reviews-mast-fm-3-1.md
    - wiki/entities/forge.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/prism-persona-research-framework.md
  source: raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 8 pages (4 concepts, 3 entities)"

- timestamp: 2026-04-08T01:38:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-strategic-human-gate-principle-10-claude-code-principles.md
    - wiki/concepts/the-strategic-human-gate-principle.md
    - wiki/concepts/rubber-stamp-approval-failure-mode.md
    - wiki/concepts/gate-placement-decision-matrix.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/prism-persona-research-framework.md
  source: raw/2026-04-08-the-strategic-human-gate-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities)"

- timestamp: 2026-04-08T01:38:56+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-token-economy-principle-10-claude-code-principles.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/concepts/cascade-escalation-pattern.md
    - wiki/concepts/adaptive-team-composition.md
    - wiki/entities/deepmind.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
    - wiki/entities/captain-agent.md
  source: raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities)"

- timestamp: 2026-04-08T01:39:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-toolkit-principle-10-claude-code-principles.md
    - wiki/concepts/the-toolkit-principle.md
    - wiki/concepts/forge-agent-assembly-framework.md
    - wiki/concepts/jig-selective-tool-loading-context-hygiene.md
    - wiki/concepts/skill-design-framework-ai-agents.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-toolkit-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities)"

- timestamp: 2026-04-08T02:54:46+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/custom-agents-in-vs-code.md
    - wiki/concepts/custom-agents-in-vs-code.md
    - wiki/concepts/agent-handoffs-in-vs-code.md
    - wiki/concepts/custom-agent-file-structure.md
    - wiki/entities/visual-studio-code.md
    - wiki/entities/github-copilot.md
  source: raw/2026-04-07-custom-agents-in-vs-code.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:16:35+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/llm-wiki.md
    - wiki/concepts/llm-maintained-persistent-wiki-pattern.md
    - wiki/concepts/llm-wiki-architecture.md
    - wiki/entities/obsidian.md
    - wiki/entities/qmd.md
    - wiki/entities/obsidian-web-clipper.md
    - wiki/entities/marp.md
    - wiki/entities/dataview.md
  source: raw/2026-04-07-llm-wiki.md
  status: success
  notes: "Auto-ingested 8 pages (2 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:22:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/htmx-html-over-the-wire.md
    - wiki/concepts/html-over-the-wire-with-htmx.md
    - wiki/concepts/htmx-attribute-api.md
    - wiki/entities/htmx.md
  source: raw/2026-04-07-test-github-repo.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:24:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system-architecture.md
    - wiki/entities/openai-gpt-4-turbo.md
    - wiki/entities/ada002.md
    - wiki/synthesis/llm-centric-architectures-operating-systems-vs-persistent-wiki-environments.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:25:59+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/transformer-architecture-note.md
    - wiki/concepts/transformer-architecture.md
    - wiki/concepts/self-attention-mechanism.md
    - wiki/concepts/multi-head-attention.md
    - wiki/concepts/positional-encoding.md
  source: raw/2026-04-07-transformer-architecture-note.md
  status: success
  notes: "Auto-ingested 5 pages (4 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:34:15+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/10-claude-code-principles-what-the-research-actually-says.md
    - wiki/concepts/the-hardening-principle.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/concepts/the-disposable-blueprint-principle.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:35:10+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/apriori-algorithm-geeksforgeeks.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/concepts/association-rule-mining.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-apriori-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:36:47+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/artificial-neural-networks-and-its-applications-geeksforgeeks.md
    - wiki/concepts/artificial-neural-network-architecture.md
    - wiki/concepts/backpropagation-learning-mechanism.md
    - wiki/concepts/activation-functions-in-neural-networks.md
    - wiki/concepts/types-of-artificial-neural-networks.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-artificial-neural-networks-and-its-applications-geeksforgeek.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:37:56+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/decision-tree-geeksforgeeks.md
    - wiki/concepts/decision-tree-algorithm.md
    - wiki/concepts/pruning-in-decision-trees.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-decision-tree-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:39:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/vision-language-action-vla-models-concepts-progress-applications-and-challenges.md
    - wiki/concepts/vision-language-action-vla-models.md
    - wiki/concepts/tokenization-and-representation-in-vla-models.md
    - wiki/concepts/multimodal-integration-in-vla-models.md
    - wiki/entities/rt-2-robotic-transformer-2.md
    - wiki/entities/cliport.md
    - wiki/entities/vima.md
  source: raw/2026-04-08-httpsarxivorgpdf250504769.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:40:27+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning.md
    - wiki/concepts/nested-learning-paradigm.md
    - wiki/concepts/hope-architecture.md
    - wiki/concepts/continuum-memory-system.md
    - wiki/entities/hope.md
    - wiki/entities/titans.md
    - wiki/entities/google-research.md
    - wiki/synthesis/transformer-vs-hope-architecture-memory-continual-learning-and-long-context-hand.md
  source: raw/2026-04-08-httpsresearchgoogleblogintroducing-nested-learning-a-new-ml-.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:41:52+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/tracing-the-thoughts-of-a-large-language-model.md
    - wiki/concepts/circuit-tracing-in-language-models.md
    - wiki/concepts/conceptual-universality-in-multilingual-language-models.md
    - wiki/concepts/faithful-vs-motivated-reasoning-in-language-models.md
    - wiki/entities/anthropic.md
    - wiki/entities/claude.md
    - wiki/synthesis/transformer-interpretability-traditional-methods-vs-circuit-tracing.md
  source: raw/2026-04-08-httpswwwanthropiccomresearchtracing-thoughts-language-model.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:42:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/implementing-the-adaboost-algorithm-from-scratch-geeksforgeeks.md
    - wiki/concepts/adaboost-algorithm.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/adaboost-vs-standalone-decision-trees-performance-and-limitations.md
  source: raw/2026-04-08-implementing-the-adaboost-algorithm-from-scratch-geeksforgee.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:43:59+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introduction-to-recurrent-neural-networks-geeksforgeeks.md
    - wiki/concepts/recurrent-neural-network-architecture.md
    - wiki/concepts/backpropagation-through-time-bptt.md
    - wiki/concepts/variants-of-recurrent-neural-networks.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/rnns-vs-transformers-handling-sequential-data-memory-and-long-term-dependencies.md
  source: raw/2026-04-08-introduction-to-recurrent-neural-networks-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:44:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/k-nearest-neighborknn-algorithm-geeksforgeeks.md
    - wiki/concepts/k-nearest-neighbor-algorithm.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/knn-vs-decision-tree-comparative-approaches-to-classification-and-regression.md
  source: raw/2026-04-08-k-nearest-neighborknn-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:46:36+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
    - wiki/concepts/lightgbm-leaf-wise-tree-growth.md
    - wiki/concepts/gradient-based-one-side-sampling-goss.md
    - wiki/concepts/histogram-based-learning-in-lightgbm.md
    - wiki/concepts/lightgbm-feature-importance-and-shap-values.md
    - wiki/entities/lightgbm.md
    - wiki/entities/microsoft.md
    - wiki/entities/shap-shapley-additive-explanations.md
    - wiki/synthesis/comparing-boosting-strategies-lightgbm-leaf-wise-adaboost-and-xgboost.md
  source: raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:47:53+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/linear-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/linear-regression.md
    - wiki/concepts/gradient-descent-in-linear-regression.md
    - wiki/concepts/regularization-techniques-in-linear-regression.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/linear-regression-vs-decision-tree-algorithms-for-regression-tasks-interpretabil.md
  source: raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:49:22+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/logistic-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/logistic-regression.md
    - wiki/concepts/sigmoid-function.md
    - wiki/concepts/maximum-likelihood-estimation-in-logistic-regression.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/linear-regression-vs-logistic-regression-mathematical-formulation-assumptions-an.md
  source: raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:51:02+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/naive-bayes-classifiers-geeksforgeeks.md
    - wiki/concepts/naive-bayes-classifier.md
    - wiki/concepts/bayes-theorem.md
    - wiki/concepts/gaussian-naive-bayes.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/naive-bayes-vs-decision-tree-assumptions-interpretability-and-performance-in-cla.md
  source: raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:51:44+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/principal-component-analysis-pca-geeksforgeeks.md
    - wiki/concepts/principal-component-analysis.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-principal-component-analysis-pca-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-08T03:53:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/random-forest-regression-in-python-geeksforgeeks.md
    - wiki/concepts/random-forest-regression.md
    - wiki/entities/randomforestregressor.md
    - wiki/entities/labelencoder.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/random-forest-regression-vs-decision-tree-algorithm-a-comparative-synthesis.md
  source: raw/2026-04-08-random-forest-regression-in-python-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:54:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/support-vector-machine-svm-algorithm-geeksforgeeks.md
    - wiki/concepts/support-vector-machine-algorithm.md
    - wiki/concepts/kernel-functions-in-svm.md
    - wiki/concepts/soft-margin-svm.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/svm-vs-decision-tree-approaches-to-classification-robustness-interpretability-an.md
  source: raw/2026-04-08-support-vector-machine-svm-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T03:57:48+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-context-hygiene-principle.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/entities/claude.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-08T04:03:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-disposable-blueprint-principle-10-claude-code-principles.md
    - wiki/concepts/the-disposable-blueprint-principle.md
    - wiki/synthesis/structured-plan-artifacts-vs-context-management-complementary-strategies-for-err.md
  source: raw/2026-04-08-the-disposable-blueprint-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 0 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:07:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-hardening-principle-10-claude-code-principles.md
    - wiki/concepts/the-hardening-principle.md
    - wiki/entities/claude.md
    - wiki/entities/ffmpeg.md
    - wiki/entities/whisper.md
    - wiki/entities/obsidian.md
  source: raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-08T04:10:09+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-institutional-memory-principle-10-claude-code-principles.md
    - wiki/concepts/the-institutional-memory-principle.md
    - wiki/entities/claude.md
    - wiki/entities/anthropic.md
    - wiki/synthesis/persistent-knowledge-codification-vs-aggressive-context-pruning-in-ai-agent-work.md
  source: raw/2026-04-08-the-institutional-memory-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:12:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-living-documentation-principle-10-claude-code-principles.md
    - wiki/concepts/the-living-documentation-principle.md
    - wiki/entities/claude.md
    - wiki/entities/architecture-decision-record-adr.md
    - wiki/synthesis/structured-automated-documentation-vs-institutional-memory-in-agentic-workflows.md
  source: raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:19:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-observability-imperative-10-claude-code-principles.md
    - wiki/concepts/the-observability-imperative.md
    - wiki/concepts/mast-failure-taxonomy.md
    - wiki/concepts/structured-artifact-chains.md
    - wiki/entities/metagpt.md
    - wiki/entities/mast-framework.md
    - wiki/entities/anthropic-building-effective-agents-guide.md
  source: raw/2026-04-08-the-observability-imperative-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-08T04:22:06+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-specialized-review-principle-10-claude-code-principles.md
    - wiki/concepts/the-specialized-review-principle.md
    - wiki/entities/forge.md
    - wiki/entities/prism-persona-science.md
    - wiki/entities/mast-failure-taxonomy.md
  source: raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-08T04:25:20+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-strategic-human-gate-principle-10-claude-code-principles.md
    - wiki/concepts/the-strategic-human-gate-principle.md
    - wiki/entities/mast-framework.md
    - wiki/entities/prism-persona-science.md
    - wiki/synthesis/strategic-human-gates-vs-specialized-review-roles-mechanisms-for-preventing-qual.md
  source: raw/2026-04-08-the-strategic-human-gate-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:29:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-token-economy-principle-10-claude-code-principles.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/entities/deepmind.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
    - wiki/synthesis/token-economy-vs-context-hygiene-optimizing-multi-agent-ai-workflows.md
  source: raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:33:57+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-toolkit-principle-10-claude-code-principles.md
    - wiki/concepts/the-toolkit-principle.md
    - wiki/concepts/skill-design-framework-for-ai-agents.md
    - wiki/concepts/selective-tool-loading-and-context-hygiene.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-toolkit-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-08T04:35:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/top-15-machine-learning-algorithms-every-data-scientist-should-know-in-2025.md
    - wiki/concepts/linear-regression-algorithm.md
    - wiki/concepts/decision-tree-algorithm.md
    - wiki/concepts/k-means-clustering-algorithm.md
    - wiki/concepts/adaboost-adaptive-boosting.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/adaboost-vs-random-forests-ensemble-learning-approaches-and-practical-trade-offs.md
  source: raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-08T04:36:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/what-is-lstm-long-short-term-memory-geeksforgeeks.md
    - wiki/concepts/long-short-term-memory-lstm.md
    - wiki/entities/geeksforgeeks.md
    - wiki/synthesis/lstms-vs-traditional-rnns-memory-retention-and-gradient-stability.md
  source: raw/2026-04-08-what-is-lstm-long-short-term-memory-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-10T12:25:44+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-lottery-ticket-hypothesis-finding-sparse-trainable-neural-networks.md
    - wiki/concepts/lottery-ticket-hypothesis.md
    - wiki/concepts/iterative-pruning-technique.md
    - wiki/concepts/initialization-sensitivity-in-sparse-neural-networks.md
    - wiki/entities/jonathan-frankle.md
    - wiki/entities/michael-carbin.md
  source: raw/2026-04-10-180303635v5pdf.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-10T12:43:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/large-language-model-reasoning-failures.md
    - wiki/concepts/taxonomy-of-llm-reasoning-failures.md
    - wiki/concepts/cognitive-biases-in-large-language-models.md
    - wiki/concepts/theory-of-mind-in-large-language-models.md
    - wiki/entities/awesome-llm-reasoning-failures-repository.md
    - wiki/synthesis/comparing-reasoning-failures-in-llms-and-human-cognitive-biases-origins-manifest.md
  source: raw/2026-04-10-260206176v1pdf.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 1 entities, 1 synthesis)"

- timestamp: 2026-04-10T12:47:06+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/axi-agent-experience-interface-github-repository.md
    - wiki/concepts/axi-design-principles-for-agent-ergonomic-cli-tools.md
    - wiki/concepts/toon-token-oriented-object-notation-format.md
    - wiki/entities/axi-agent-experience-interface.md
    - wiki/entities/toon-token-oriented-object-notation.md
    - wiki/entities/gh-axi.md
    - wiki/entities/chrome-devtools-axi.md
  source: raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
  status: success
  notes: "Auto-ingested 7 pages (2 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-10T12:48:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoskills-github-repository.md
    - wiki/concepts/automated-ai-skill-stack-installation.md
    - wiki/concepts/supply-chain-security-hardening-for-ai-agent-projects.md
    - wiki/concepts/claude-code-skill-summarization.md
    - wiki/entities/autoskills.md
    - wiki/entities/skills-sh.md
    - wiki/entities/claude-code.md
  source: raw/2026-04-10-httpsgithubcommidudevautoskills.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-10T17:25:20+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/recursive-language-models.md
    - wiki/concepts/recursive-language-models.md
    - wiki/entities/rlm-qwen3-8b.md
    - wiki/entities/gpt-5.md
    - wiki/entities/qwen3-coder-480b-a35b.md
  source: raw/2026-04-10-251224601v2pdf.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-11T02:53:59+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/mempalace-github-repository.md
    - wiki/concepts/palace-memory-architecture.md
    - wiki/concepts/aaak-compression-dialect.md
    - wiki/concepts/contradiction-detection-utility.md
    - wiki/entities/mempalace.md
    - wiki/entities/aaak-compression-dialect.md
    - wiki/entities/chromadb.md
    - wiki/entities/mcp-mempalace-control-protocol.md
    - wiki/synthesis/spatially-organized-memory-vs-llm-maintained-persistent-wiki-long-term-ai-recall.md
  source: raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 4 entities, 1 synthesis)"

- timestamp: 2026-04-12T00:44:42+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoagent-fully-automated-and-zero-code-llm-agent-framework-hkudsautoagent-githu.md
    - wiki/concepts/natural-language-driven-agent-building.md
    - wiki/concepts/self-managing-workflow-generation.md
    - wiki/concepts/intelligent-resource-orchestration.md
    - wiki/entities/autoagent.md
    - wiki/entities/metachain.md
    - wiki/synthesis/democratizing-agent-customization-automated-skill-stack-installation-vs-natural-.md
  source: raw/2026-04-12-httpsgithubcomhkudsautoagent.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-12T00:44:59+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoagent-fully-automated-and-zero-code-llm-agent-framework-github-repository.md
    - wiki/concepts/natural-language-driven-agent-creation.md
    - wiki/concepts/self-managing-workflow-generation.md
    - wiki/concepts/intelligent-resource-orchestration-for-llm-agents.md
    - wiki/entities/autoagent.md
    - wiki/entities/hkuds.md
    - wiki/synthesis/comparing-axis-cli-ergonomics-with-autoagents-natural-language-driven-agent-crea.md
  source: raw/2026-04-12-httpsgithubcomhkudsautoagent-1.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-13T13:32:01+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/chrome-devtools-mcp-github-repository.md
    - wiki/concepts/model-context-protocol-mcp-server-for-chrome-devtools.md
    - wiki/concepts/agent-ergonomic-tool-design-principles.md
    - wiki/concepts/chrome-devtools-mcp-cli-interface.md
    - wiki/entities/chrome-devtools-mcp.md
    - wiki/entities/puppeteer.md
    - wiki/entities/chrome-devtools.md
    - wiki/synthesis/comparing-chrome-devtools-mcp-and-axi-for-agentic-tool-integration-protocol-vs-e.md
  source: raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-13T16:35:11+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/amitshekhariitbhullm-internals-learn-llm-internals-step-by-step.md
    - wiki/concepts/byte-pair-encoding-bpe-in-large-language-models.md
    - wiki/concepts/attention-mechanism-in-large-language-models.md
    - wiki/concepts/kv-cache-and-paged-attention-in-large-language-models.md
    - wiki/concepts/flash-attention-in-large-language-models.md
    - wiki/entities/amit-shekhar.md
    - wiki/entities/outcome-school.md
    - wiki/entities/llm-internals.md
    - wiki/synthesis/standard-attention-vs-flash-attention-in-llms-efficiency-scalability-and-deploym.md
  source: raw/2026-04-13-amitshekhariitbhullm-internals-learn-llm-internals-step-by-s.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-13T17:25:49+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/timesfm-time-series-foundation-model-google-researchtimesfm.md
    - wiki/concepts/time-series-foundation-model-architecture.md
    - wiki/concepts/agent-skill-integration-for-time-series-forecasting.md
    - wiki/concepts/continuous-quantile-forecasting-in-time-series-models.md
    - wiki/entities/timesfm.md
    - wiki/entities/google-research.md
  source: raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-13T17:58:02+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/nousresearchautoreason-autoresearch-for-subjective-domains.md
    - wiki/concepts/autoreason-iterative-self-refinement-framework.md
    - wiki/entities/autoreason.md
    - wiki/entities/shl0ms.md
    - wiki/entities/hermes-agent.md
    - wiki/synthesis/autoreason-vs-critique-and-revise-structural-approaches-to-bias-scope-creep-and-.md
  source: raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-13T18:01:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/hope-a-memory-architecture-for-continual-learning-with-long-contexts.md
    - wiki/concepts/hope-architecture.md
  source: raw/2026-04-13-260406231v1pdf.md
  status: success
  notes: "Auto-ingested 2 pages (1 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-14T00:23:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/legal-rag-hallucinations.md
    - wiki/concepts/hallucinations-in-legal-retrieval-augmented-generation-rag-systems.md
  source: raw/2026-04-14-legal_rag_hallucinationspdf.md
  status: success
  notes: "Auto-ingested 2 pages (1 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-16T19:27:53+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/entities/ace-agentic-context-engineering.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-17T15:37:23+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/watcher-e2e-validation.md
    - wiki/concepts/end-to-end-validation-in-live-memory-loops.md
    - wiki/entities/mempalace-watcher.md
    - wiki/entities/mempalace.md
  source: raw/2026-04-17-watcher-e2e-validation.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"
```

## [2026-04-17] curator-merge | duplicate concept consolidation
- targets:
  - wiki/concepts/linear-regression.md (canonical, absorbed linear-regression-algorithm)
  - wiki/concepts/llm-wiki-architecture.md (canonical, absorbed llm-maintained-persistent-wiki-pattern)
- removed:
  - wiki/concepts/linear-regression-algorithm.md (same algorithm, different source)
  - wiki/concepts/llm-maintained-persistent-wiki-pattern.md (same source_hash dc3efe98…)
- rewired all `[[Linear Regression Algorithm]]` and `[[LLM-Maintained Persistent Wiki Pattern]]` references across 9 pages
- added bidirectional `[[Attention Mechanism in Large Language Models]]` ↔ `[[Transformer Architecture]]` link to merge graph communities 2 and 9
- agent: copilot-cli (manual graph review)
- status: success
- notes: index.md regeneration + graph rebuild to follow

## [2026-04-17] curator-merge | wiki review + graph hardening (Karpathy LLM-wiki alignment)

Findings → fixes across the wiki + graph stack to align with Karpathy's
[gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) on
LLM-maintained persistent wikis (compile-once, file-back, lateral linking).

**Phase 1 — manual merges + missing cross-refs**
- Merged duplicate concepts: `linear-regression-algorithm` → `linear-regression`,
  `llm-maintained-persistent-wiki-pattern` → `llm-wiki-architecture` (both pairs
  shared an identical `source_hash`). All references swept via sed across 9
  files. Two duplicate files deleted.
- Added bidirectional `[[Transformer Architecture]] ↔ [[Attention Mechanism in
  Large Language Models]]` cross-link plus Flash-Attention / KV-Cache /
  Positional-Encoding `related:` entries.

**Phase 2 — graph builder bug fix**
- `wiki-graph-api/graph_builder.py`: previously parsed `[[wikilinks]]` from the
  body only, **silently dropping every `related:` frontmatter link**. Now
  regex-scans the frontmatter section too. After cache-bust + rebuild,
  Transformer & Attention land in the same community for the first time.

**Phase 3 — auto-ingest fuzzy dedup**
- `scripts/auto_ingest.py`: added `rapidfuzz` (≥3.0) gate before creating any
  new concept/entity page. If `token_set_ratio >= 85` against an existing title,
  the new content is merged into the existing page instead of forking.
- Tested in container: `"linear regression"` vs `"linear regression algorithm"`
  → 100.0. Future ingests will not recreate the dups we just merged.

**Phase 4 — agent prompt upgrades**
- `wiki-curator.agent.md`: graph-aware gap analysis (uses /graph/communities,
  /graph/god-nodes, /graph/surprises), bridge-detection between communities,
  publisher-smell warning, canonical log-prefix convention
  `## [YYYY-MM-DD] op | Title`.
- `wiki-lint.agent.md`: new error classes (duplicate `source_hash`, fuzzy-dup
  titles ≥85), new warnings (graph orphans degree=0, implicit concepts, missing
  `related:` body mentions, god-node publishers).
- `wiki-query.agent.md`: file-back loop — every answer that exposes a wiki gap
  drafts a capture target or proposes a `related:` cross-link, logged as
  `query-fileback`. Read-only → read-and-compound, per Karpathy.

**Phase 5 — publisher demotion**
- `graph_builder.py`: edges touching publisher entities (geeksforgeeks, arxiv,
  github, youtube, …) get weight 0.1 instead of 1.0. Hosting links no longer
  pull unrelated topics into the same modularity cluster. Communities split
  more naturally (18 → 20).

**Operational also:** chowned 56 root-owned wiki files back to `jbl:jbl`
(auto-ingest container had been writing as root — fixable later with
`user:` directive in compose).

**Verify with:** `curl -s http://graph-api.jbl-lab.com/graph/stats | jq` and
`grep "^## \[" wiki/log.md | tail -10`.

- timestamp: 2026-04-18T01:37:52+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-mobile-graph-ui-wiki-dedup.md
    - wiki/concepts/mobile-first-graph-ui-design-for-wiki-systems.md
    - wiki/concepts/wiki-concept-deduplication-and-canonicalization.md
    - wiki/concepts/agentic-wiki-optimization-karpathy-compile-once-principles.md
    - wiki/entities/karpathy-compile-once-wiki-principle.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:38:48+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-56-no-retrain-fixes-planning.md
    - wiki/concepts/artifact-registry-validation-in-ml-pipelines.md
    - wiki/concepts/stat-exclusion-policy-in-ml-prediction-pipelines.md
    - wiki/entities/nba-ml-model-registry.md
    - wiki/entities/pra-composite-prediction.md
  source: raw/2026-04-18-copilot-session-sprint-56-no-retrain-fixes-planning-895454cb.md
  status: success
  notes: "Auto-ingested 5 pages (2 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:38:50+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-mobile-graph-ui-wiki-dedup.md
    - wiki/concepts/mobile-first-graph-ui-design-for-wiki-systems.md
    - wiki/concepts/wiki-deduplication-and-concept-merging-in-llm-wikis.md
    - wiki/concepts/agentic-workflow-optimization-for-llm-wikis.md
    - wiki/entities/graph-jbl-lab.md
    - wiki/entities/labs-wiki.md
    - wiki/synthesis/complementarity-and-competition-exact-source-hash-deduplication-vs-fuzzy-concept.md
  source: raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 2 entities, 1 synthesis)"

- timestamp: 2026-04-18T01:38:56+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-homepage-overhaul-and-resource-tuning.md
    - wiki/concepts/homelab-service-inventory-and-dashboard-synchronization.md
    - wiki/concepts/container-resource-tuning-and-performance-remediation.md
    - wiki/concepts/database-indexing-for-performance-optimization.md
    - wiki/entities/mempalace.md
    - wiki/entities/qdrant.md
    - wiki/entities/knightcrawler.md
  source: raw/2026-04-18-copilot-session-homepage-overhaul-and-resource-tuning-79cdb38d.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:39:43+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis.md
    - wiki/concepts/ensemble-model-save-round-trip-validation-gate.md
    - wiki/concepts/root-cause-analysis-silent-ensemble-model-save-failures.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/ensemblemodel.md
    - wiki/entities/labs-wiki.md
  source: raw/2026-04-18-copilot-session-sprint-57-ensemble-save-diagnosis-e2943da5.md
  status: success
  notes: "Auto-ingested 6 pages (2 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:39:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-nba-ml-oom-fix-and-docs-cleanup.md
    - wiki/concepts/container-resource-tuning-and-performance-remediation.md
    - wiki/concepts/agent-documentation-hygiene-and-migration.md
    - wiki/entities/nba-ml-model-registry.md
    - wiki/entities/mempalace.md
    - wiki/entities/openmemory.md
  source: raw/2026-04-18-copilot-session-nba-ml-oom-fix-and-docs-cleanup-52d24b9f.md
  status: success
  notes: "Auto-ingested 6 pages (2 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:39:56+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis.md
    - wiki/concepts/atomic-model-artifact-saving-in-ml-training-loops.md
    - wiki/concepts/ensemble-model-save-round-trip-validation-gate.md
    - wiki/concepts/root-cause-analysis-of-silent-model-artifact-save-failures.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/ensemblemodel.md
    - wiki/entities/minutesmodel.md
  source: raw/2026-04-18-copilot-session-sprint-57-ensemble-save-diagnosis-e2943da5.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:40:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-58-shap-bug-planning.md
    - wiki/concepts/shap-analysis-bug-resolution-in-nba-ml-engine.md
    - wiki/concepts/atomic-save-pattern-for-model-artifacts.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/modelregistry.md
    - wiki/entities/ensemblemodel.md
    - wiki/synthesis/shap-explainability-across-tree-based-linear-and-ensemble-models-in-production-m.md
  source: raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
  status: success
  notes: "Auto-ingested 7 pages (2 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-18T01:41:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-55-implementation-and-deployment.md
    - wiki/concepts/parallel-agent-coordination-ml-sprint-implementation.md
    - wiki/concepts/calibration-leakage-mitigation-ml-model-training.md
    - wiki/concepts/edge-gating-stat-specific-thresholds-ml-prediction-pipelines.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/labs-wiki.md
  source: raw/2026-04-18-copilot-session-sprint-55-implementation-and-deployment-2d04e4e0.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:42:11+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-59-shap-coverage-implementation.md
    - wiki/concepts/shap-coverage-extension-for-ridge-and-ensemble-models.md
    - wiki/concepts/atomic-model-artifact-saving-via-atomic-pickle-dump.md
    - wiki/concepts/registry-health-snapshot-tracking-and-dashboard-integration.md
    - wiki/entities/shap-shapley-additive-explanations.md
    - wiki/entities/ensemblemodel.md
    - wiki/entities/ridgemodel.md
  source: raw/2026-04-18-copilot-session-sprint-59-shap-coverage-implementation-9a231f70.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:42:31+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-58-shap-bug-planning.md
    - wiki/concepts/shap-analysis-bug-root-cause-and-remediation.md
    - wiki/concepts/atomic-save-pattern-for-model-artifacts.md
    - wiki/concepts/registry-health-validation-via-scheduled-cron.md
    - wiki/entities/shap-shapley-additive-explanations.md
    - wiki/entities/modelregistry.md
    - wiki/entities/nba-ml-engine.md
    - wiki/synthesis/shap-explainability-standard-lightgbm-vs-custom-serialized-models-in-production.md
  source: raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 3 entities, 1 synthesis)"

- timestamp: 2026-04-18T01:43:36+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-55-planning-and-exploration.md
    - wiki/concepts/parallel-agent-coordination-ml-sprint-implementation.md
    - wiki/concepts/context-aware-imputation-ml-pipelines.md
    - wiki/concepts/calibration-leakage-mitigation-ml-model-training.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/mlflow-api.md
    - wiki/entities/nba-ml-model-registry.md
  source: raw/2026-04-18-copilot-session-sprint-55-planning-and-exploration-be98e3c5.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T01:45:15+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-training-status-tracker-and-oom-fix.md
    - wiki/concepts/training-pipeline-status-tracking-ml-systems.md
    - wiki/concepts/oom-failure-diagnosis-remediation-ml-containers.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/nba-ml-api.md
    - wiki/entities/minutesmodel.md
    - wiki/entities/qdrant.md
  source: raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  status: success
  notes: "Auto-ingested 7 pages (2 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T02:16:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-session-wiki-promotion.md
    - wiki/concepts/durable-copilot-session-checkpoint-promotion.md
    - wiki/concepts/source-aware-model-routing-wiki-ingestion-pipelines.md
    - wiki/entities/mempalace.md
    - wiki/entities/karpathy-compile-once-wiki-principle.md
  source: raw/2026-04-18-copilot-session-session-wiki-promotion-405414ae.md
  status: success
  notes: "Auto-ingested 5 pages (2 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T02:52:52+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-fixing-mempalace-timeouts.md
    - wiki/concepts/mempalace-timeout-database-lock-remediation.md
    - wiki/concepts/durable-copilot-session-checkpoint-promotion.md
    - wiki/entities/mempalace.md
    - wiki/entities/chromadb.md
    - wiki/entities/mempalace-watcher.md
    - wiki/entities/mcp-mempalace-control-protocol.md
  source: raw/2026-04-18-copilot-session-fixing-mempalace-timeouts-d94dbf3b.md
  status: success
  notes: "Auto-ingested 7 pages (2 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:24:31+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-auto-ingest-pipeline-built-and-docs-updated.md
    - wiki/concepts/auto-ingest-pipeline-for-wiki-markdown-processing.md
    - wiki/entities/github-models-api.md
    - wiki/entities/docker.md
    - wiki/entities/python-watchdog-library.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-auto-ingest-pipeline-built-and-docs-updated-f3b54c4f.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:28:04+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-fixing-android-share-ingest-api.md
    - wiki/concepts/universal-ingest-endpoint-for-flexible-api-request-parsing.md
    - wiki/concepts/http-shortcuts-android-app-scripting-api-quirks.md
    - wiki/concepts/auto-type-detection-in-api-ingest-requests.md
    - wiki/entities/http-shortcuts.md
    - wiki/entities/labs-wiki-ingest-api.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:35:05+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-mempalace-phase-3-4-and-autoagent-research.md
    - wiki/concepts/mempalace-phase-3-4-features-and-implementation.md
    - wiki/concepts/autoagent-framework-research.md
    - wiki/entities/mempalace.md
    - wiki/entities/autoagent.md
    - wiki/entities/chromadb.md
    - wiki/entities/litellm.md
    - wiki/entities/docker.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-mempalace-phase-3-4-and-autoagent-research-5bfd2570.md
  status: success
  notes: "Auto-ingested 8 pages (2 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:36:35+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-nba-ml-agents-and-homelab-fixes.md
    - wiki/concepts/nba-ml-specialized-prediction-agents.md
    - wiki/concepts/sprint-workflow-integration-for-ai-agents.md
    - wiki/concepts/adguard-memory-oom-diagnosis-and-fix.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/copilot-cli.md
    - wiki/entities/adguard.md
    - wiki/entities/knightcrawler.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:37:25+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-ntfy-notifications-galloping-bot-alerts-monitor-fixes.md
    - wiki/concepts/ntfy-push-notifications-for-service-monitoring.md
    - wiki/concepts/caddy-handle-path-directive-and-url-token-injection.md
    - wiki/concepts/docker-container-resource-auditing-and-optimization.md
    - wiki/concepts/uptime-kuma-monitor-authentication-and-notification-integration.md
    - wiki/entities/ntfy.md
    - wiki/entities/caddy.md
    - wiki/entities/uptime-kuma.md
    - wiki/entities/knightcrawler.md
    - wiki/entities/galloping-bot.md
    - wiki/entities/docker.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
  status: success
  notes: "Auto-ingested 11 pages (4 concepts, 6 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:38:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-odds-api-quota-optimization-sgo-investigation.md
    - wiki/concepts/odds-api-quota-optimization.md
    - wiki/concepts/cascading-pipeline-failure-diagnosis-and-resilience.md
    - wiki/concepts/sportsgameodds-sgo-api-data-extraction-challenges.md
    - wiki/entities/odds-api.md
    - wiki/entities/sportsgameodds-sgo-api.md
    - wiki/entities/mlflow-api.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:38:22+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-optimizing-snipe-book-then-retry-flow.md
    - wiki/concepts/book-then-retry-booking-flow-optimization.md
    - wiki/entities/galloping-bot.md
    - wiki/entities/ezlinks-api.md
    - wiki/entities/durable-copilot-session-checkpoint.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:38:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-phases-1-4-implementation-and-deployment.md
    - wiki/concepts/batch-prediction-optimization-nba-ml-engine.md
    - wiki/concepts/dashboard-expansion-player-profile-waiver-wire-data-health.md
    - wiki/concepts/database-query-performance-hardening-nba-ml-platform.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/ensemblemodel.md
    - wiki/entities/streamlit-dashboard.md
    - wiki/entities/timescaledb.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-phases-1-4-implementation-and-deployment-16041f82.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:39:37+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-pipeline-enhancements-and-vision-support-deployed.md
    - wiki/concepts/auto-ingest-pipeline-for-llm-powered-knowledge-wiki.md
    - wiki/concepts/smart-url-handlers-twitter-x-github-repositories.md
    - wiki/concepts/vision-support-in-llm-knowledge-ingestion-using-gpt-4-1.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/github-models-api.md
    - wiki/entities/fxtwitter-api.md
    - wiki/entities/gpt-4-1.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-enhancements-and-vision-support-deploye-5028ddea.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:41:16+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-pipeline-resilience-fixes-dashboard-metrics-investiga.md
    - wiki/concepts/pipeline-resilience-in-machine-learning-systems.md
    - wiki/concepts/dashboard-metrics-consistency-and-hit-rate-discrepancy-analysis.md
    - wiki/concepts/mlflow-resilience-and-fallback-mechanisms-in-model-training.md
    - wiki/entities/mlflow-api.md
    - wiki/entities/nba-ml-prediction-pipeline.md
    - wiki/entities/odds-api.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:41:50+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-planning-and-progress-tracking-complete.md
    - wiki/concepts/llm-wiki-architecture.md
    - wiki/concepts/multi-device-source-ingestion-architecture.md
    - wiki/concepts/phased-implementation-planning-progress-tracking-llm-wikis.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/claude.md
    - wiki/entities/obra-superpowers-skills.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-planning-and-progress-tracking-complete-d09b537d.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:42:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-props-db-query-and-chart-refinement.md
    - wiki/concepts/backend-for-frontend-pattern-in-modern-dashboard-architecture.md
    - wiki/concepts/handling-postgresql-numeric-type-in-nodejs-pg-library.md
    - wiki/concepts/dashboard-chart-strategy-and-data-driven-refinement.md
    - wiki/concepts/replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/express-js.md
    - wiki/entities/fastapi.md
    - wiki/entities/postgresql.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:43:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-rankings-page-and-performance-optimization.md
    - wiki/concepts/backend-for-frontend-pattern-in-modern-dashboard-architecture.md
    - wiki/concepts/replacing-lateral-joins-with-regular-join-case-for-performance-optimization.md
    - wiki/concepts/server-side-in-memory-caching-with-ttl-for-api-performance.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/express-js.md
    - wiki/entities/postgresql.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:43:42+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-react-dashboard-scaffold-and-pages-built.md
    - wiki/concepts/backend-for-frontend-pattern-in-modern-dashboard-architecture.md
    - wiki/concepts/react-dashboard-redesign-typescript-tailwindcss.md
    - wiki/concepts/taste-skill-design-system-ui-consistency.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/express-5.md
    - wiki/entities/fastapi.md
    - wiki/entities/tailwind-css-4.md
    - wiki/entities/vite.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:44:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-researching-mempalace-for-comparison-doc.md
    - wiki/concepts/mempalace-memory-system.md
    - wiki/concepts/comparison-mempalace-labs-wiki-openmemory.md
    - wiki/entities/mempalace.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/openmemory.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md
  status: success
  notes: "Auto-ingested 6 pages (2 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:44:46+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-resource-optimization-opencode-bash-fix.md
    - wiki/concepts/caddy-handle-path-directive-and-its-impact-on-upstream-url-construction.md
    - wiki/concepts/opencode-bash-shell-configuration-posix-spawn-enoent-fix.md
    - wiki/concepts/docker-container-resource-auditing-and-optimization.md
    - wiki/entities/knightcrawler.md
    - wiki/entities/opencode.md
    - wiki/entities/caddy.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-resource-optimization-opencode-bash-fix-c00d8543.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:45:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-retrained-models-deploying-improvements.md
    - wiki/concepts/nba-ml-prediction-platform-sprint-workflow.md
    - wiki/concepts/ensemblemodel-stacking-meta-learner.md
    - wiki/concepts/edge-gating-stat-specific-thresholds-ml-prediction-pipelines.md
    - wiki/concepts/homelab-server-deployment-nba-ml-platform.md
    - wiki/entities/ensemblemodel.md
    - wiki/entities/homelab.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:46:25+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-reworking-docs-for-copilotopencode.md
    - wiki/concepts/mempalace-architecture-and-migration.md
    - wiki/concepts/copilot-cli-opencode-integration-with-mempalace.md
    - wiki/concepts/homelab-infrastructure-patterns-for-ai-memory-migration.md
    - wiki/entities/mempalace.md
    - wiki/entities/copilot-cli.md
    - wiki/entities/opencode.md
    - wiki/entities/openmemory.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/homelab.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
  status: success
  notes: "Auto-ingested 10 pages (3 concepts, 6 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:46:48+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sgo-data-extraction-fix-and-quality-audit.md
    - wiki/concepts/sportsgameodds-sgo-api-data-extraction-challenges.md
    - wiki/entities/sportsgameodds-sgo-api.md
    - wiki/entities/durable-copilot-session-checkpoint.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:47:25+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-10-complete-and-deployed.md
    - wiki/concepts/feature-engineering-nba-ml-engine-sprint-10.md
    - wiki/concepts/warmstarting-hyperparameter-tuning-optuna.md
    - wiki/concepts/quantile-crossing-fix-xgboost-lightgbm.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/optuna.md
    - wiki/entities/docker.md
    - wiki/entities/lightgbm.md
    - wiki/entities/xgboost.md
    - wiki/entities/catboost.md
    - wiki/entities/ensemblemodel.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-complete-and-deployed-cb380016.md
  status: success
  notes: "Auto-ingested 11 pages (3 concepts, 7 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:48:12+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-10-implementation-and-deployment.md
    - wiki/concepts/quantile-crossing-fix-gradient-boosting-models.md
    - wiki/concepts/warmstarting-hyperparameter-tuning-optuna.md
    - wiki/concepts/target-encoding-shifted-expanding-mean-time-series.md
    - wiki/concepts/feature-engineering-nba-ml-engine-sprint-10.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/optuna.md
    - wiki/entities/xgboost.md
    - wiki/entities/lightgbm.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-implementation-and-deployment-693c9264.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:48:57+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-10-retrain-in-progress.md
    - wiki/concepts/feature-engineering-nba-player-performance-modeling.md
    - wiki/concepts/warmstarting-hyperparameter-tuning-optuna.md
    - wiki/concepts/quantile-crossing-fix-uncertainty-prediction.md
    - wiki/entities/optuna.md
    - wiki/entities/xgboost.md
    - wiki/entities/lightgbm.md
    - wiki/entities/nba-ml-engine.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:49:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-10-retrain-in-progress.md
    - wiki/concepts/quantile-crossing-fix-gradient-boosting-models.md
    - wiki/concepts/warmstarting-hyperparameter-tuning-optuna.md
    - wiki/concepts/target-encoding-shifted-expanding-mean-time-series.md
    - wiki/concepts/per-stat-model-selection-and-ensemble-learning-nba-ml-engine.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/optuna.md
    - wiki/entities/lightgbm.md
    - wiki/entities/xgboost.md
    - wiki/entities/catboost.md
    - wiki/entities/modelregistry.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
  status: success
  notes: "Auto-ingested 11 pages (4 concepts, 6 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:49:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-11-evaluation-and-report.md
    - wiki/concepts/holdout-evaluator-module.md
    - wiki/concepts/feature-alignment-for-feature-selection-models.md
    - wiki/concepts/calibration-analysis-for-regression-models.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/lstm-model.md
    - wiki/entities/holdout-evaluator-cli-command.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:49:40+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-11-evaluation-and-report.md
    - wiki/concepts/holdout-evaluator-module.md
    - wiki/concepts/lstm-gating-mechanism-nba-ml-engine.md
    - wiki/concepts/feature-alignment-for-feature-selection-models.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/durable-copilot-session-checkpoint.md
    - wiki/entities/homelab.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:50:10+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed.md
    - wiki/concepts/feature-group-tuning-via-configuration-flags.md
    - wiki/concepts/per-statistic-calibration-percentiles.md
    - wiki/concepts/persistence-of-residuals-in-model-save-load.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/taste-skill-package.md
    - wiki/entities/node-version-manager-nvm.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:50:19+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed.md
    - wiki/concepts/sprint-12-nba-ml-engine-code-cleanup-feature-tuning.md
    - wiki/concepts/per-stat-calibration-fixes-residual-persistence-model-save-load.md
    - wiki/concepts/walk-forward-stability-analysis-backtesting-nba-ml-engine.md
    - wiki/concepts/nodejs-installation-nvm-global-taste-skill-installation.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/node-version-manager-nvm.md
    - wiki/entities/taste-skill-package.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
  status: success
  notes: "Auto-ingested 8 pages (4 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:50:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-13-model-improvements-code.md
    - wiki/concepts/minutes-prediction-sub-model.md
    - wiki/concepts/edge-threshold-optimizer-kelly-criterion.md
    - wiki/concepts/dynamic-ensemble-weighting.md
    - wiki/concepts/binary-over-under-classifier.md
    - wiki/entities/minutesmodel.md
    - wiki/entities/overunderclassifier.md
    - wiki/entities/edge-optimizer.md
    - wiki/entities/ensemblemodel.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T03:51:02+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-13-model-improvements-code.md
    - wiki/concepts/minutes-prediction-sub-model.md
    - wiki/concepts/edge-threshold-optimizer-kelly-criterion.md
    - wiki/concepts/dynamic-ensemble-weighting.md
    - wiki/concepts/binary-over-under-classifier.md
    - wiki/entities/minutesmodel.md
    - wiki/entities/overunderclassifier.md
    - wiki/entities/edge-optimizer.md
    - wiki/entities/ensemblemodel.md
  source: raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-18T12:13:21+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/dive-into-claude-code-the-design-space-of-todays-and-future-ai-agent-systems.md
    - wiki/concepts/layered-agentic-architecture-claude-code.md
    - wiki/concepts/human-centric-design-values-principles-agent-systems.md
    - wiki/concepts/context-management-compaction-pipeline-claude-code.md
    - wiki/entities/claude-code.md
    - wiki/entities/openclaw.md
    - wiki/entities/anthropic.md
  source: raw/2026-04-18-260414228v1pdf.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T12:14:02+00:00
  operation: checkpoint-cluster-synthesis
  agent: auto-ingest
  targets:
    - wiki/synthesis/recurring-checkpoint-patterns-durable-copilot-session-checkpoint-promotion-auto-.md
    - wiki/synthesis/recurring-checkpoint-patterns-caddy-handle-path-directive-and-its-impact-on-upst.md
    - wiki/synthesis/recurring-checkpoint-patterns-parallel-agent-coordination-in-ml-sprint-implement.md
    - wiki/synthesis/recurring-checkpoint-patterns-odds-api-quota-optimization-cascading-pipeline-fai.md
    - wiki/synthesis/recurring-checkpoint-patterns-backend-for-frontend-bff-pattern-in-modern-dashboa.md
    - wiki/synthesis/recurring-checkpoint-patterns-feature-engineering-for-nba-ml-engine-sprint-10-wa.md
  source: plans/checkpoint-curation-phase5-report.md
  status: success
  notes: "Backfill synthesis pages for checkpoint merge clusters"

- timestamp: 2026-04-18T12:23:17+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/dive-into-claude-code-the-design-space-of-todays-and-future-ai-agent-systems.md
    - wiki/concepts/layered-agentic-architecture-claude-code.md
    - wiki/concepts/design-principles-agentic-coding-tools.md
    - wiki/concepts/comparative-agent-system-architecture-claude-code-vs-openclaw.md
    - wiki/entities/claude-code.md
    - wiki/entities/openclaw.md
    - wiki/entities/anthropic.md
  source: raw/2026-04-18-260414228v1pdf.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-18T15:48:35+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-phase-5-merged-graph-ui-next.md
    - wiki/concepts/durable-copilot-session-checkpoint-promotion.md
    - wiki/concepts/full-corpus-wikilink-cleanup-lint-resolution.md
    - wiki/concepts/synthesis-batch-runner-merge-cluster-backlog.md
    - wiki/entities/durable-copilot-session-checkpoint.md
  source: raw/2026-04-18-copilot-session-phase-5-merged-graph-ui-next-48f23b63.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-18T22:37:40+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-knightcrawler-done-routing-traced.md
    - wiki/concepts/knightcrawler-cron-automation-monitoring-status-tracking.md
    - wiki/concepts/homelab-media-domain-routing-lan-public-https-diagnostics.md
    - wiki/concepts/diagnosing-browser-automation-failures-containerized-web-services.md
    - wiki/entities/knightcrawler.md
    - wiki/entities/opencode.md
    - wiki/entities/caddy.md
    - wiki/entities/cloudflare.md
  source: raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-19T14:59:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/6372438pdf.md
  source: raw/2026-04-19-6372438pdf.md
  status: success
  notes: "Auto-ingested 1 pages (0 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-19T15:33:30+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-60-pts-feature-planning.md
    - wiki/concepts/pts-feature-engineering-opponent-defensive-rating-rolling-window.md
    - wiki/concepts/teammate-injured-usage-delta-feature.md
    - wiki/concepts/classifier-stats-extension-calibration-audit.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/sgo-sportsgameodds-api.md
  source: raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-19T22:54:18+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-sprint-61-planning-audit.md
    - wiki/concepts/pickle-load-audit-across-base-model-classes.md
    - wiki/concepts/pts-feature-interaction-engineering.md
    - wiki/concepts/stl-edge-threshold-audit-backtesting.md
    - wiki/entities/nba-ml-engine.md
  source: raw/2026-04-19-copilot-session-sprint-61-planning-audit-6c5cb258.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-20T00:23:49+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-scheduler-dns-agents-cleanup.md
    - wiki/concepts/stale-training-status-detection-remediation-ml-pipelines.md
    - wiki/concepts/split-dns-routing-cloudflare-tunnel-overrides-homelab-services.md
    - wiki/concepts/agent-skill-surface-optimization-multi-tool-ai-project-compatibility.md
    - wiki/entities/nba-ml-engine.md
    - wiki/entities/homelab.md
    - wiki/entities/ofelia-scheduler.md
    - wiki/entities/adguard.md
  source: raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T03:13:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/cloudflare-launches-code-mode-mcp-server-to-optimize-token-usage-for-ai-agents.md
    - wiki/concepts/code-mode-mcp-server.md
    - wiki/concepts/token-footprint-optimization-agent-api-integration.md
    - wiki/concepts/secure-sandbox-execution-agentic-workflows.md
    - wiki/entities/cloudflare.md
    - wiki/entities/code-mode-mcp-server.md
  source: raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T03:15:56+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-wiki-audit-followups.md
    - wiki/concepts/planning-only-checkpoint-suppression-wiki-auto-ingest-pipelines.md
    - wiki/concepts/orphan-pruning-mempalace-sync-scripts.md
    - wiki/concepts/heuristic-based-classification-session-checkpoints.md
  source: raw/2026-04-20-copilot-session-wiki-audit-followups-92b1089b.md
  status: success
  notes: "Auto-ingested 4 pages (3 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-20T03:21:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-implementing-checkpoint-curation-phases.md
    - wiki/concepts/durable-copilot-session-checkpoint-promotion.md
    - wiki/concepts/heuristic-based-classification-session-checkpoints.md
    - wiki/entities/checkpoint-classifier-module.md
  source: raw/2026-04-18-copilot-session-implementing-checkpoint-curation-phases-625f7a54.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-20T03:22:12+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-phase-5-backfill-script-written.md
    - wiki/concepts/backfill-script-copilot-session-checkpoint-curation.md
    - wiki/concepts/quality-score-normalization-wiki-session-checkpoints.md
    - wiki/entities/backfill-checkpoint-curation-script.md
    - wiki/entities/checkpoint-classifier-module.md
  source: raw/2026-04-18-copilot-session-phase-5-backfill-script-written-6227b6ae.md
  status: success
  notes: "Auto-ingested 5 pages (2 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T11:12:01+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-second-curation-reports.md
    - wiki/concepts/graph-aware-editorial-scoring-wiki-checkpoint-curation.md
    - wiki/concepts/clean-worktree-based-development-wiki-curation-pipelines.md
    - wiki/concepts/robust-path-resolution-wiki-curation-scripts.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/homelab.md
    - wiki/entities/scripts-backfill-checkpoint-curation-py.md
  source: raw/2026-04-20-copilot-session-second-curation-reports-23bcd48f.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-20T11:37:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agents-that-remember-introducing-agent-memory.md
    - wiki/concepts/palace-memory-architecture.md
    - wiki/concepts/agent-memory-ingestion-pipeline.md
    - wiki/concepts/agent-memory-retrieval-pipeline.md
    - wiki/entities/agent-memory.md
    - wiki/entities/cloudflare.md
    - wiki/entities/durable-object.md
    - wiki/entities/vectorize.md
    - wiki/entities/workers-ai.md
  source: raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:27:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agents-that-remember-introducing-agent-memory.md
    - wiki/concepts/agent-memory-ingestion-pipeline.md
    - wiki/concepts/agent-memory-retrieval-pipeline.md
    - wiki/concepts/memory-supersession-chains.md
    - wiki/entities/agent-memory.md
    - wiki/entities/cloudflare.md
    - wiki/entities/durable-object.md
    - wiki/entities/vectorize.md
    - wiki/entities/workers-ai.md
  source: raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:29:16+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
    - wiki/concepts/lightgbm-leaf-wise-tree-growth.md
    - wiki/concepts/gradient-based-one-side-sampling-goss.md
    - wiki/concepts/histogram-based-learning-in-lightgbm.md
    - wiki/concepts/lightgbm-hyperparameter-tuning.md
    - wiki/entities/lightgbm.md
    - wiki/entities/microsoft.md
  source: raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:30:20+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/entities/agentic-context-engineering-ace.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 7 pages (2 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:33:17+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/entities/ace-agentic-context-engineering.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:36:11+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/incremental-delta-updates.md
    - wiki/entities/ace-agentic-context-engineering.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:50:02+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/incremental-delta-updates.md
    - wiki/entities/ace-agentic-context-engineering.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:51:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/incremental-delta-updates.md
    - wiki/entities/ace-agentic-context-engineering.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T19:04:37+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agents-that-remember-introducing-agent-memory.md
    - wiki/concepts/agent-memory-ingestion-pipeline.md
    - wiki/concepts/agent-memory-retrieval-pipeline.md
    - wiki/concepts/memory-supersession-chains.md
    - wiki/concepts/hybrid-retrieval-agent-memory-systems.md
    - wiki/entities/agent-memory.md
    - wiki/entities/cloudflare.md
    - wiki/entities/durable-object.md
    - wiki/entities/vectorize.md
    - wiki/entities/workers-ai.md
  source: raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
  status: success
  notes: "Auto-ingested 10 pages (4 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-20T19:05:55+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
    - wiki/concepts/lightgbm-leaf-wise-tree-growth.md
    - wiki/concepts/gradient-based-one-side-sampling-goss.md
    - wiki/concepts/histogram-based-learning-in-lightgbm.md
    - wiki/concepts/lightgbm-hyperparameter-tuning.md
    - wiki/entities/lightgbm.md
    - wiki/entities/microsoft.md
  source: raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T19:08:46+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/brevity-bias-context-collapse-llm-context-adaptation.md
    - wiki/concepts/incremental-delta-updates.md
    - wiki/concepts/grow-and-refine-mechanism-context-engineering.md
    - wiki/entities/ace-agentic-context-engineering.md
    - wiki/entities/appworld-benchmark.md
    - wiki/entities/finer.md
    - wiki/entities/deepseek-v3-1.md
  source: raw/2026-04-16-251004618v3pdf.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T23:16:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/dive-into-claude-code-the-design-space-of-todays-and-future-ai-agent-systems.md
    - wiki/concepts/layered-agentic-architecture-claude-code.md
    - wiki/concepts/layered-agentic-architecture-claude-code.md
    - wiki/concepts/context-management-compaction-pipeline-claude-code.md
    - wiki/entities/claude-code.md
    - wiki/entities/openclaw.md
    - wiki/entities/anthropic.md
  source: raw/2026-04-18-260414228v1pdf.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-20T23:17:54+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/proxy-pointer-rag-structure-meets-scale-at-100-accuracy-with-smarter-retrieval.md
    - wiki/concepts/proxy-pointer-rag-architecture.md
    - wiki/concepts/structure-guided-chunking-breadcrumb-injection.md
    - wiki/concepts/two-stage-retrieval-structural-llm-re-ranking.md
    - wiki/entities/proxy-pointer.md
    - wiki/entities/gemini-flash-lite.md
    - wiki/entities/faiss.md
    - wiki/entities/llamaparse.md
  source: raw/2026-04-20-proxy-pointer-rag-structure-meets-scale-at-100-accuracy-with.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T23:19:27+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/amitshekhariitbhullm-internals-learn-llm-internals-step-by-step.md
    - wiki/concepts/byte-pair-encoding-bpe-in-large-language-models.md
    - wiki/concepts/attention-mechanism-in-large-language-models.md
    - wiki/concepts/kv-cache-and-paged-attention-in-large-language-models.md
    - wiki/concepts/flash-attention-in-large-language-models.md
    - wiki/entities/amit-shekhar.md
    - wiki/entities/outcome-school.md
    - wiki/entities/llm-internals.md
  source: raw/2026-04-13-amitshekhariitbhullm-internals-learn-llm-internals-step-by-s.md
  status: success
  notes: "Auto-ingested 8 pages (4 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-20T23:21:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/10-claude-code-principles-what-the-research-actually-says.md
    - wiki/concepts/the-hardening-principle.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/concepts/the-living-documentation-principle.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/entities/claude.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
  status: success
  notes: "Auto-ingested 8 pages (4 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:02:27+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/chrome-devtools-mcp-github-repository.md
    - wiki/concepts/model-context-protocol-mcp-server-for-chrome-devtools.md
    - wiki/concepts/chrome-devtools-mcp-cli-interface.md
    - wiki/concepts/design-principles-agentic-coding-tools.md
    - wiki/entities/chrome-devtools-mcp.md
  source: raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:03:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/artificial-neural-networks-and-its-applications-geeksforgeeks.md
    - wiki/concepts/artificial-neural-network-architecture.md
    - wiki/concepts/backpropagation-learning-mechanism.md
    - wiki/concepts/activation-functions-in-neural-networks.md
    - wiki/concepts/types-of-artificial-neural-networks.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-artificial-neural-networks-and-its-applications-geeksforgeek.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:05:20+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/mempalace-github-repository.md
    - wiki/concepts/mempalace-memory-system.md
    - wiki/concepts/closet-index-layer.md
    - wiki/concepts/source-adapter-plugin-specification.md
    - wiki/entities/mempalace.md
    - wiki/entities/chromadb.md
  source: raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:06:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/vision-language-action-vla-models-concepts-progress-applications-and-challenges.md
    - wiki/concepts/vision-language-action-vla-models.md
    - wiki/concepts/multimodal-integration-in-vla-models.md
    - wiki/concepts/tokenization-and-representation-in-vla-models.md
    - wiki/entities/cliport.md
    - wiki/entities/rt-2-robotic-transformer-2.md
    - wiki/entities/gato.md
  source: raw/2026-04-08-httpsarxivorgpdf250504769.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:07:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning.md
    - wiki/concepts/nested-learning-paradigm.md
    - wiki/concepts/continuum-memory-system.md
    - wiki/concepts/hope-architecture.md
    - wiki/entities/hope.md
    - wiki/entities/titans.md
    - wiki/entities/google-research.md
  source: raw/2026-04-08-httpsresearchgoogleblogintroducing-nested-learning-a-new-ml-.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:10:03+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-observability-imperative-10-claude-code-principles.md
    - wiki/concepts/the-observability-imperative.md
    - wiki/concepts/mast-failure-taxonomy.md
    - wiki/concepts/structured-artifact-chains.md
    - wiki/entities/metagpt.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/anthropic-building-effective-agents-guide.md
  source: raw/2026-04-08-the-observability-imperative-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:28:30+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoskills-github-repository.md
    - wiki/concepts/automated-ai-skill-stack-installation.md
    - wiki/concepts/supply-chain-security-hardening-for-ai-agent-projects.md
    - wiki/concepts/universal-agent-schema-agents-md-for-ai-tool-integration.md
    - wiki/entities/autoskills.md
    - wiki/entities/skills-sh.md
    - wiki/entities/claude-code.md
    - wiki/entities/fendo.md
  source: raw/2026-04-10-httpsgithubcommidudevautoskills.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-21T02:06:16+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/tracing-the-thoughts-of-a-large-language-model.md
    - wiki/concepts/circuit-tracing-in-language-models.md
    - wiki/concepts/conceptual-universality-in-multilingual-language-models.md
    - wiki/concepts/faithful-vs-motivated-reasoning-in-language-models.md
    - wiki/entities/anthropic.md
    - wiki/entities/claude.md
    - wiki/entities/claude.md
  source: raw/2026-04-08-httpswwwanthropiccomresearchtracing-thoughts-language-model.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T03:06:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-toolkit-principle-10-claude-code-principles.md
    - wiki/concepts/the-toolkit-principle.md
    - wiki/concepts/forge-science-backed-agent-assembly-system.md
    - wiki/concepts/selective-tool-loading-and-context-hygiene.md
    - wiki/concepts/skill-design-framework-for-ai-agents.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-toolkit-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 7 pages (4 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T04:06:23+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-lottery-ticket-hypothesis-finding-sparse-trainable-neural-networks.md
    - wiki/concepts/lottery-ticket-hypothesis.md
    - wiki/concepts/iterative-pruning-technique.md
    - wiki/concepts/initialization-sensitivity-in-sparse-neural-networks.md
    - wiki/entities/jonathan-frankle.md
    - wiki/entities/michael-carbin.md
  source: raw/2026-04-10-180303635v5pdf.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T05:06:41+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoagent-fully-automated-and-zero-code-llm-agent-framework-hkudsautoagent-githu.md
    - wiki/concepts/natural-language-driven-agent-building.md
    - wiki/concepts/self-managing-workflow-generation.md
    - wiki/concepts/intelligent-resource-orchestration.md
    - wiki/entities/autoagent.md
    - wiki/entities/metachain.md
    - wiki/entities/hkuds.md
  source: raw/2026-04-12-httpsgithubcomhkudsautoagent.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T06:06:19+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/timesfm-time-series-foundation-model-google-researchtimesfm.md
    - wiki/concepts/timesfm-model-architecture.md
    - wiki/concepts/agent-skill-integration-for-time-series-forecasting.md
    - wiki/concepts/forecastconfig-forecasting-configuration-abstraction.md
    - wiki/entities/timesfm.md
    - wiki/entities/google-research.md
  source: raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T07:06:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/introduction-to-recurrent-neural-networks-geeksforgeeks.md
    - wiki/concepts/recurrent-neural-network-architecture.md
    - wiki/concepts/backpropagation-through-time-bptt.md
    - wiki/concepts/variants-of-recurrent-neural-networks.md
    - wiki/concepts/variants-of-recurrent-neural-networks.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-introduction-to-recurrent-neural-networks-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T08:06:12+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/linear-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/linear-regression.md
    - wiki/concepts/gradient-descent-in-linear-regression.md
    - wiki/concepts/regularization-techniques-in-linear-regression.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T09:06:37+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/logistic-regression-in-machine-learning-geeksforgeeks.md
    - wiki/concepts/logistic-regression.md
    - wiki/concepts/sigmoid-function.md
    - wiki/concepts/maximum-likelihood-estimation-in-logistic-regression.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T10:06:50+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/large-language-model-reasoning-failures.md
    - wiki/concepts/taxonomy-of-llm-reasoning-failures.md
    - wiki/concepts/cognitive-biases-in-large-language-models.md
    - wiki/concepts/theory-of-mind-in-large-language-models.md
    - wiki/concepts/fundamental-cognitive-skills-executive-function-failures-llms.md
    - wiki/entities/awesome-llm-reasoning-failures-repository.md
    - wiki/entities/peiyang-song.md
    - wiki/entities/pengrui-han.md
    - wiki/entities/noah-goodman.md
  source: raw/2026-04-10-260206176v1pdf.md
  status: success
  notes: "Auto-ingested 9 pages (4 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-21T11:06:44+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/axi-agent-experience-interface-kunchenguidaxi-github-repository.md
    - wiki/concepts/axi-design-principles-for-agent-ergonomic-cli-tools.md
    - wiki/concepts/toon-token-oriented-object-notation-format.md
    - wiki/entities/axi-agent-experience-interface.md
    - wiki/entities/gh-axi.md
    - wiki/entities/chrome-devtools-axi.md
  source: raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
  status: success
  notes: "Auto-ingested 6 pages (2 concepts, 3 entities, 0 synthesis)"
- timestamp: 2026-04-20T13:28:55+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-graph-tracker-and-depth-review.md
    - wiki/concepts/graph-aware-checkpoint-tracker-implementation.md
    - wiki/concepts/synthesis-layer-depth-audit-extraction-bottleneck-analysis.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/wiki-graph-api-graph-builder-py.md
    - wiki/entities/reports-checkpoint-graph-tracker-md.md
  source: raw/2026-04-20-copilot-session-graph-tracker-and-depth-review-4445c933.md
  status: success
  notes: "Auto-ingested 6 pages (2 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-20T17:36:10+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-integrating-agent-skill-routing.md
    - wiki/concepts/agent-skill-routing-architecture.md
    - wiki/concepts/worktree-based-subagent-driven-development.md
    - wiki/concepts/automated-skill-path-generation-containerized-agent-systems.md
    - wiki/entities/agent-skills-for-context-engineering.md
    - wiki/entities/update-opencode-skills-paths-py.md
  source: raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
  status: success
  notes: "Auto-ingested 6 pages (3 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:26:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-pilot-worktree-baseline.md
    - wiki/concepts/worktree-based-baseline-verification-durable-workflow-pilots.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/scripts-auto-ingest-py.md
  source: raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-20T18:52:05+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/leworldmodel-stable-end-to-end-joint-embedding-predictive-architecture-from-pixe.md
    - wiki/concepts/leworldmodel-architecture.md
    - wiki/concepts/sketched-isotropic-gaussian-regularizer-sigreg.md
    - wiki/concepts/latent-planning-leworldmodel.md
    - wiki/entities/leworldmodel.md
    - wiki/entities/sketched-isotropic-gaussian-regularizer-sigreg.md
    - wiki/entities/pldm.md
    - wiki/entities/dino-wm.md
  source: raw/2026-04-20-260319312v2pdf.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-20T20:25:07+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-url-followup-pass.md
    - wiki/concepts/content-root-selection-article-extraction.md
    - wiki/concepts/image-ranking-extraction-article-content.md
    - wiki/concepts/validation-run-policy-audit-log-suppression.md
    - wiki/entities/labs-wiki.md
    - wiki/entities/scripts-auto-ingest-py.md
    - wiki/entities/github-models-api.md
  source: raw/2026-04-20-copilot-session-url-followup-pass-b53bba3e.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T00:28:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/copilot-session-checkpoint-free-tier-backfill-runner.md
    - wiki/concepts/free-tier-constrained-backfill-runner-design.md
    - wiki/concepts/homelab-cron-job-integration-throttled-ingestion.md
    - wiki/entities/tmp-free-tier-url-backfill-py.md
  source: raw/2026-04-21-copilot-session-free-tier-backfill-runner-a2d20186.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T01:26:10+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/memento-extending-llm-output-length-via-blockwise-summarization-and-kv-cache-com.md
    - wiki/concepts/memento-blockwise-summarization-for-llms.md
    - wiki/entities/memento.md
    - wiki/entities/memento.md
    - wiki/entities/openmementos-dataset.md
    - wiki/entities/microsoft.md
  source: raw/2026-04-21-httpsgithubcommicrosoftmemento.md
  status: success
  notes: "Auto-ingested 6 pages (1 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-21T02:45:25+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/adams-law-textual-frequency-law-on-large-language-models.md
    - wiki/concepts/textual-frequency-law-tfl.md
    - wiki/concepts/textual-frequency-distillation-tfd.md
    - wiki/concepts/curriculum-textual-frequency-training-ctft.md
    - wiki/entities/textual-frequency-paired-dataset-tfpd.md
    - wiki/entities/facemind-corporation.md
    - wiki/entities/the-chinese-university-of-hong-kong.md
  source: raw/2026-04-21-260402176v2pdf.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:09:27+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/custom-agents-in-vs-code.md
    - wiki/concepts/custom-agents-in-vs-code.md
    - wiki/concepts/agent-handoffs-in-vs-code.md
    - wiki/concepts/custom-agent-file-structure.md
    - wiki/entities/visual-studio-code.md
  source: raw/2026-04-07-custom-agents-in-vs-code.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:10:09+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/jbl306homelab.md
    - wiki/concepts/homelab-infrastructure-patterns-for-ai-memory-migration.md
    - wiki/entities/homelab.md
  source: raw/2026-04-07-jbl306homelab.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:11:08+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/llm-wiki.md
    - wiki/concepts/karpathy-llm-wiki-pattern.md
    - wiki/concepts/llm-wiki-architecture.md
    - wiki/entities/obsidian.md
    - wiki/entities/qmd.md
    - wiki/entities/obsidian-web-clipper.md
    - wiki/entities/dataview.md
    - wiki/entities/marp.md
  source: raw/2026-04-07-llm-wiki.md
  status: success
  notes: "Auto-ingested 8 pages (2 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:11:39+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/htmx-html-over-the-wire.md
    - wiki/concepts/html-over-the-wire-with-htmx.md
    - wiki/entities/htmx.md
  source: raw/2026-04-07-test-github-repo.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:12:36+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system-architecture.md
    - wiki/entities/openai-gpt-4-turbo.md
    - wiki/entities/ada002.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:13:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/apriori-algorithm-geeksforgeeks.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-apriori-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:14:31+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/decision-tree-geeksforgeeks.md
    - wiki/concepts/decision-tree-algorithm.md
    - wiki/concepts/splitting-criteria-in-decision-trees.md
    - wiki/concepts/pruning-in-decision-trees.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-decision-tree-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:15:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/implementing-the-adaboost-algorithm-from-scratch-geeksforgeeks.md
    - wiki/concepts/adaboost-algorithm.md
    - wiki/entities/adaboost.md
    - wiki/entities/decisiontreeclassifier.md
    - wiki/entities/scikit-learn.md
  source: raw/2026-04-08-implementing-the-adaboost-algorithm-from-scratch-geeksforgee.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:15:57+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/k-nearest-neighborknn-algorithm-geeksforgeeks.md
    - wiki/concepts/k-nearest-neighbor-algorithm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-k-nearest-neighborknn-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:17:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/naive-bayes-classifiers-geeksforgeeks.md
    - wiki/concepts/naive-bayes-classifier.md
    - wiki/concepts/gaussian-naive-bayes.md
    - wiki/concepts/multinomial-naive-bayes.md
    - wiki/concepts/bernoulli-naive-bayes.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:18:25+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/principal-component-analysis-pca-geeksforgeeks.md
    - wiki/concepts/principal-component-analysis.md
    - wiki/entities/geeksforgeeks.md
    - wiki/entities/scikit-learn.md
  source: raw/2026-04-08-principal-component-analysis-pca-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:19:27+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/random-forest-regression-in-python-geeksforgeeks.md
    - wiki/concepts/random-forest-regression.md
    - wiki/entities/randomforestregressor.md
    - wiki/entities/labelencoder.md
    - wiki/entities/scikit-learn.md
  source: raw/2026-04-08-random-forest-regression-in-python-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:21:23+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/support-vector-machine-svm-algorithm-geeksforgeeks.md
    - wiki/concepts/support-vector-machine-algorithm.md
    - wiki/entities/scikit-learn.md
    - wiki/entities/support-vector-classifier-svc.md
    - wiki/entities/breast-cancer-dataset.md
  source: raw/2026-04-08-support-vector-machine-svm-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:22:30+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-context-hygiene-principle-10-claude-code-principles.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/concepts/u-shaped-attention-curve-transformer-models.md
    - wiki/concepts/progressive-disclosure-context-loading.md
    - wiki/concepts/context-poisoning-llm-workflows.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 6 pages (4 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:23:01+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-disposable-blueprint-principle-10-claude-code-principles.md
    - wiki/concepts/the-disposable-blueprint-principle.md
  source: raw/2026-04-08-the-disposable-blueprint-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 2 pages (1 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:23:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-hardening-principle-10-claude-code-principles.md
    - wiki/concepts/the-hardening-principle.md
  source: raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 2 pages (1 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:24:00+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-institutional-memory-principle-10-claude-code-principles.md
    - wiki/concepts/the-institutional-memory-principle.md
  source: raw/2026-04-08-the-institutional-memory-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 2 pages (1 concepts, 0 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:24:34+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-living-documentation-principle-10-claude-code-principles.md
    - wiki/concepts/the-living-documentation-principle.md
    - wiki/entities/architecture-decision-record-adr.md
    - wiki/entities/claude-md.md
  source: raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:26:42+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/custom-agents-in-vs-code.md
    - wiki/concepts/custom-agents-in-vs-code.md
    - wiki/concepts/agent-handoffs-in-vs-code.md
    - wiki/concepts/custom-agent-file-structure.md
    - wiki/entities/visual-studio-code.md
  source: raw/2026-04-07-custom-agents-in-vs-code.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:27:41+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/jbl306homelab.md
    - wiki/concepts/homelab-server-deployment-nba-ml-platform.md
    - wiki/concepts/split-dns-routing-cloudflare-tunnel-overrides-homelab-services.md
    - wiki/concepts/comprehensive-grafana-monitoring-for-docker-homelab-services.md
    - wiki/entities/homelab.md
  source: raw/2026-04-07-jbl306homelab.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:28:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/llm-wiki.md
    - wiki/concepts/karpathy-llm-wiki-pattern.md
    - wiki/concepts/schema-guided-llm-knowledge-base-maintenance.md
    - wiki/concepts/contradiction-detection-utility.md
    - wiki/entities/obsidian.md
    - wiki/entities/obsidian-web-clipper.md
    - wiki/entities/marp.md
    - wiki/entities/dataview.md
    - wiki/entities/qmd.md
  source: raw/2026-04-07-llm-wiki.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:29:19+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/htmx-html-over-the-wire.md
    - wiki/concepts/html-over-the-wire-with-htmx.md
    - wiki/entities/htmx.md
  source: raw/2026-04-07-test-github-repo.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:29:58+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/karpathy-llm-os-tweet.md
    - wiki/concepts/llm-operating-system-architecture.md
    - wiki/entities/openai-gpt-4-turbo.md
    - wiki/entities/ada002.md
  source: raw/2026-04-07-test-tweet.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:30:57+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/apriori-algorithm-geeksforgeeks.md
    - wiki/concepts/apriori-algorithm.md
    - wiki/concepts/association-rule-mining.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-apriori-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:32:06+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/decision-tree-geeksforgeeks.md
    - wiki/concepts/decision-tree-algorithm.md
    - wiki/concepts/splitting-criteria-in-decision-trees.md
    - wiki/concepts/pruning-in-decision-trees.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-decision-tree-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:32:59+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/implementing-the-adaboost-algorithm-from-scratch-geeksforgeeks.md
    - wiki/concepts/adaboost-algorithm.md
    - wiki/entities/adaboost.md
    - wiki/entities/decisiontreeclassifier.md
    - wiki/entities/scikit-learn.md
  source: raw/2026-04-08-implementing-the-adaboost-algorithm-from-scratch-geeksforgee.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:33:29+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/k-nearest-neighborknn-algorithm-geeksforgeeks.md
    - wiki/concepts/k-nearest-neighbor-algorithm.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-k-nearest-neighborknn-algorithm-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:34:20+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/naive-bayes-classifiers-geeksforgeeks.md
    - wiki/concepts/naive-bayes-classifier.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:35:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/principal-component-analysis-pca-geeksforgeeks.md
    - wiki/concepts/principal-component-analysis.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-principal-component-analysis-pca-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 3 pages (1 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:37:05+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-specialized-review-principle-10-claude-code-principles.md
    - wiki/concepts/the-specialized-review-principle.md
    - wiki/entities/forge.md
    - wiki/entities/prism-persona-science.md
    - wiki/entities/mast-failure-taxonomy.md
  source: raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:37:46+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-strategic-human-gate-principle-10-claude-code-principles.md
    - wiki/concepts/the-strategic-human-gate-principle.md
    - wiki/entities/mast-failure-taxonomy.md
    - wiki/entities/prism-persona-science.md
    - wiki/entities/forge.md
  source: raw/2026-04-08-the-strategic-human-gate-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:38:22+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/the-token-economy-principle-10-claude-code-principles.md
    - wiki/concepts/the-token-economy-principle.md
    - wiki/entities/deepmind.md
    - wiki/entities/forge.md
    - wiki/entities/jig.md
  source: raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:39:26+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/what-is-lstm-long-short-term-memory-geeksforgeeks.md
    - wiki/concepts/long-short-term-memory-lstm.md
    - wiki/concepts/lstm-gating-mechanism-nba-ml-engine.md
    - wiki/entities/geeksforgeeks.md
  source: raw/2026-04-08-what-is-lstm-long-short-term-memory-geeksforgeeks.md
  status: success
  notes: "Auto-ingested 4 pages (2 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:40:32+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/recursive-language-models.md
    - wiki/concepts/recursive-language-models.md
    - wiki/entities/rlm-qwen3-8b.md
    - wiki/entities/qwen3-coder-480b-a35b.md
  source: raw/2026-04-10-251224601v2pdf.md
  status: success
  notes: "Auto-ingested 4 pages (1 concepts, 2 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:41:45+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoagent-fully-automated-and-zero-code-llm-agent-framework-hkudsautoagent-githu.md
    - wiki/concepts/natural-language-driven-agent-building.md
    - wiki/concepts/self-managing-workflow-generation.md
    - wiki/concepts/intelligent-resource-orchestration.md
    - wiki/entities/autoagent.md
    - wiki/entities/metachain.md
    - wiki/entities/hkuds.md
  source: raw/2026-04-12-httpsgithubcomhkudsautoagent-1.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:42:47+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/autoagent-fully-automated-and-zero-code-llm-agent-framework-hkudsautoagent-githu.md
    - wiki/concepts/natural-language-driven-agent-building.md
    - wiki/concepts/self-managing-workflow-generation.md
    - wiki/concepts/intelligent-resource-orchestration.md
    - wiki/entities/autoagent.md
    - wiki/entities/metachain.md
    - wiki/entities/hkuds.md
  source: raw/2026-04-12-httpsgithubcomhkudsautoagent-2.md
  status: success
  notes: "Auto-ingested 7 pages (3 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:44:14+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/hope-a-memory-architecture-for-continual-learning-with-long-contexts.md
    - wiki/concepts/hope-architecture.md
    - wiki/concepts/memento-blockwise-summarization-for-llms.md
    - wiki/concepts/catastrophic-forgetting-mitigation-continual-learning.md
    - wiki/entities/hope.md
    - wiki/entities/pengrui-han.md
    - wiki/entities/peiyang-song.md
    - wiki/entities/noah-goodman.md
    - wiki/entities/michael-carbin.md
  source: raw/2026-04-13-260406231v1pdf.md
  status: success
  notes: "Auto-ingested 9 pages (3 concepts, 5 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:44:49+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/nousresearchautoreason-autoresearch-for-subjective-domains.md
    - wiki/concepts/autoreason-iterative-self-refinement-framework.md
    - wiki/entities/autoreason.md
    - wiki/entities/shl0ms.md
    - wiki/entities/hermes-agent.md
  source: raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:45:51+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/legal-rag-hallucinations.md
    - wiki/concepts/hallucinations-in-legal-retrieval-augmented-generation-rag-systems.md
    - wiki/concepts/hallucinations-in-legal-retrieval-augmented-generation-rag-systems.md
    - wiki/concepts/typology-legal-hallucinations-correctness-groundedness.md
    - wiki/entities/lexisnexis-lexis-plus-ai.md
    - wiki/entities/thomson-reuters-westlaw-ai-assisted-research.md
    - wiki/entities/thomson-reuters-ask-practical-law-ai.md
    - wiki/entities/openai-gpt-4-turbo.md
  source: raw/2026-04-14-legal_rag_hallucinationspdf.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:46:33+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/6372438pdf.md
    - wiki/concepts/agentic-context-engineering-ace.md
    - wiki/concepts/the-context-hygiene-principle.md
    - wiki/concepts/memory-supersession-chains.md
    - wiki/entities/agentic-context-engineering-ace.md
  source: raw/2026-04-19-6372438pdf.md
  status: success
  notes: "Auto-ingested 5 pages (3 concepts, 1 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:48:06+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/leworldmodel-stable-end-to-end-joint-embedding-predictive-architecture-from-pixe.md
    - wiki/concepts/leworldmodel-architecture.md
    - wiki/concepts/sketched-isotropic-gaussian-regularizer-sigreg.md
    - wiki/concepts/latent-planning-leworldmodel.md
    - wiki/entities/leworldmodel.md
    - wiki/entities/sketched-isotropic-gaussian-regularizer-sigreg.md
    - wiki/entities/pldm.md
    - wiki/entities/dino-wm.md
  source: raw/2026-04-20-260319312v2pdf.md
  status: success
  notes: "Auto-ingested 8 pages (3 concepts, 4 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:49:24+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/adams-law-textual-frequency-law-on-large-language-models.md
    - wiki/concepts/textual-frequency-law-tfl.md
    - wiki/concepts/textual-frequency-distillation-tfd.md
    - wiki/concepts/curriculum-textual-frequency-training-ctft.md
    - wiki/concepts/textual-frequency-paired-dataset.md
    - wiki/entities/textual-frequency-paired-dataset-tfpd.md
    - wiki/entities/facemind-corporation.md
    - wiki/entities/the-chinese-university-of-hong-kong.md
  source: raw/2026-04-21-260402176v2pdf.md
  status: success
  notes: "Auto-ingested 8 pages (4 concepts, 3 entities, 0 synthesis)"

- timestamp: 2026-04-21T13:49:57+00:00
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/sources/memento-github-repository.md
    - wiki/concepts/memento-blockwise-summarization-for-llms.md
    - wiki/entities/memento.md
    - wiki/entities/openmementos-dataset.md
    - wiki/entities/microsoft.md
  source: raw/2026-04-21-httpsgithubcommicrosoftmemento.md
  status: success
  notes: "Auto-ingested 5 pages (1 concepts, 3 entities, 0 synthesis)"
```
