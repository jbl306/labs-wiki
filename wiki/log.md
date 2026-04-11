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
```
