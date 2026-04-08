---
title: "Circuit Tracing in Language Models"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "37dca25e4ed5998ae5f1377fbae32da1d785a06990c5f9e00b16c9ac74c66bd1"
sources:
  - raw/2026-04-08-httpswwwanthropiccomresearchtracing-thoughts-language-model.md
quality_score: 0
concepts:
  - circuit-tracing-in-language-models
related:
  - "[[Activation Functions in Neural Networks]]"
  - "[[Artificial Neural Network Architecture]]"
  - "[[Tracing the Thoughts of a Large Language Model]]"
tier: hot
tags: [interpretability, neuroscience-inspired, causal-analysis, language-models, AI-safety]
---

# Circuit Tracing in Language Models

## Overview

Circuit tracing is an interpretability technique for large language models that identifies and links interpretable features into computational circuits, revealing how input words are transformed into output. Inspired by neuroscience, this method allows researchers to probe, manipulate, and understand the internal pathways responsible for reasoning, planning, and decision-making in models like Claude.

## How It Works

Circuit tracing begins by locating interpretable features—distinct patterns of neural activation corresponding to concepts or behaviors—within a language model. These features are then linked together into circuits, which represent the computational pathways that process information from input to output. The process draws inspiration from neuroscience, where researchers map neural activity to understand cognition.

To trace circuits, researchers use tools that can intervene in the model's internal state. For example, they may pinpoint the activation corresponding to a concept (such as 'rabbit' in a poem) and modify or suppress it, observing how the model's output changes. This allows for causal analysis: if removing a concept alters the output, it is part of the computational pathway for that behavior.

Circuit tracing can reveal parallel pathways. In mental math, Claude uses one path for rough approximation and another for precise digit calculation, combining them for the final answer. Researchers can intervene in these paths to see how each contributes to the computation, and whether the model relies on memorization or algorithmic reasoning.

The method also enables tracing multi-step reasoning. When answering questions like 'What is the capital of the state where Dallas is located?', circuit tracing shows Claude first activates features for 'Dallas is in Texas', then for 'capital of Texas is Austin', demonstrating compositional reasoning rather than rote memorization.

By manipulating intermediate steps, researchers can test the model's reliance on these circuits. Swapping 'Texas' for 'California' changes the answer from 'Austin' to 'Sacramento', confirming the model's use of multi-step reasoning. Circuit tracing thus provides a window into the actual computational logic behind model outputs, rather than relying on surface explanations.

## Key Properties

- **Causal Intervention:** Researchers can manipulate internal features to test their causal role in output generation.
- **Parallel Pathways:** Circuit tracing reveals multiple computational paths working in tandem, such as approximation and precision in math.
- **Compositional Reasoning:** The method uncovers how models combine independent facts to answer complex questions.
- **Scalability Challenge:** Current circuit tracing methods are labor-intensive and only capture a fraction of computation, especially in long prompts.

## Limitations

Circuit tracing is currently limited by the complexity and scale of modern language models. It requires significant human effort to interpret circuits, and only a small portion of the total computation is captured. Artifacts from the tools used may distort the true underlying mechanisms. Scaling to thousands of words and more complex reasoning chains will require methodological improvements and possibly AI-assisted analysis.

## Example

In poetry generation, researchers identified the 'rabbit' concept in Claude's internal state before it wrote the second line of a poem. By suppressing this concept, Claude chose a different rhyme ('habit'). Injecting 'green' led to a line ending with 'green', showing causal control over planning.

## Visual

The included diagram shows a stylized circuit network, with nodes and connections highlighted in blue, representing the traced computational pathways inside a language model.

## Relationship to Other Concepts

- **[[Activation Functions in Neural Networks]]** — Activation functions determine the patterns of neural activity that circuit tracing seeks to interpret.
- **[[Artificial Neural Network Architecture]]** — Circuit tracing operates within the architecture of neural networks, mapping pathways between layers and units.

## Practical Applications

Circuit tracing can audit AI reasoning for reliability and alignment, flagging fabricated explanations, motivated reasoning, and concerning behaviors. It is useful for transparency in safety-critical domains, such as medical imaging and genomics, where understanding model internals can reveal scientific insights.

## Sources

- [[Tracing the Thoughts of a Large Language Model]] — primary source for this concept
