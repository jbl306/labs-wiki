---
title: 'amitshekhariitbhu/llm-internals: Learn LLM internals step by step - from tokenization
  to attention to inference optimization.'
type: url
captured: 2026-04-13 16:33:58.346896+00:00
source: android-share
url: https://github.com/amitshekhariitbhu/llm-internals
content_hash: sha256:891ca4dfd5e2d5be2dfffe03ddb33bfa19ec320d89363f9c0d7bae719c9c58e8
tags: []
status: ingested
last_refreshed: '2026-04-22T02:45:00+00:00'
---

https://github.com/amitshekhariitbhu/llm-internals

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:45:00+00:00
- source_url: https://github.com/amitshekhariitbhu/llm-internals
- resolved_url: https://github.com/amitshekhariitbhu/llm-internals
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: amitshekhariitbhu/llm-internals
Description: Learn LLM internals step by step - from tokenization to attention to inference optimization.
Stars: 605
Language: None
Topics: attention-is-all-you-need, attention-mechanism, large-language-models, learn-llm, llm, llm-internals

## README

<p align="center">
    <img alt="AI Engineering Interview Questions and Answers" src="https://github.com/amitshekhariitbhu/llm-internals/blob/main/assets/banner.png">
</p>

# LLM Internals

**Learn LLM internals step by step - from tokenization to attention to inference optimization.**

---

Prepared and maintained by the **Founder** of Outcome School: [Amit Shekhar](https://x.com/amitiitbhu)

---

**Note: This series will continue to grow as I write more blogs and create more videos on new topics. Keep learning.**

---

## Large Language Models (LLMs)

Before diving into the internals of an LLM, it’s a good idea to first understand what an LLM actually is.

In this video, we will cover the following:

* LLM
* RAG
* MCP
* Agent
* Fine-tuning
* Quantization

Let's get started: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)

---

## Tokenization in Large Language Models (LLMs)

In this video, we will learn about Tokenization and why they are essential for Large Language Models.

Let's get started: [Tokenization in Large Language Models (LLMs)](https://www.youtube.com/watch?v=sK2s9I84EVI)

---


## Byte Pair Encoding in LLMs

In this blog, we will learn about BPE (Byte Pair Encoding) - the tokenization algorithm used by most modern Large Language Models (LLMs) to break text into smaller pieces before processing it.

We will understand what BPE is, why it is needed, and how it works step by step with a simple example.

We will cover the following:

* What is Tokenization?
* The Problem: How to Break Text into Tokens?
* What is BPE (Byte Pair Encoding)?
* How BPE Works: Step by Step
* How BPE Tokenizes New Text
* Why BPE is Used in Modern LLMs

Let's get started: [Byte Pair Encoding in LLMs](https://outcomeschool.com/blog/bpe-in-llms)

---

## Math behind Attention - Q, K, and V

In this blog, we will learn about the math behind Attention: Query(Q), Key(K), and Value(V) with a step-by-step numeric example.

We will cover the following:

* The Attention Formula
* Setting Up: From Words to Vectors
* Creating Q, K, and V Matrices
* Computing Attention Scores (Q x K^T)
* Scaling the Scores
* Applying Softmax
* Computing the Final Output (Attention Weights x V)
* Putting It All Together

Let's get started: [Math behind Attention - Q, K, and V](https://outcomeschool.com/blog/math-behind-attention-qkv)

---

## Math behind √dₖ Scaling Factor in Attention

In this blog, we will learn about why we scale the dot product attention by √dₖ in the Transformer architecture with a step-by-step numeric example.

We will cover the following:

* The Attention Formula (Quick Recap)
* What Happens Without Scaling?
* Why Do Dot Products Grow with dₖ?
* Understanding Variance of the Dot Product
* Proving It Step by Step: Variance of the Dot Product is dₖ
* What Large Dot Products Do to Softmax
* Why √dₖ is the Right Scaling Factor
* Seeing It with Real Numbers
* Putting It All Together

Let's get started: [Math behind √dₖ Scaling Factor in Attention](https://outcomeschool.com/blog/scaling-dot-product-attention)

---

## Causal Masking in Attention

In this blog, we will learn about causal masking in attention.

We will start with the introduction of causal masking, understand the problem of seeing future tokens through an example, and then walk through its implementation to see how masked attention prevents the model from accessing future tokens.

We will cover the following:

* Without Causal Masking
* With Causal Masking
* Implementation of Causal Masking
* The Causal Mask Matrix

Let's get started: [Causal Masking in Attention](https://outcomeschool.com/blog/causal-masking-in-attention)

---

## Math Behind Backpropagation

In this blog, we will learn about the math behind backpropagation in neural networks.

Backpropagation is the core algorithm that allows neural networks to learn from their mistakes. Without it, training neural networks efficiently would not be possible. Understanding the math behind it gives us a deeper understanding of how neural networks actually learn. Do not worry, we will learn about each concept step by step so that everything is clear.

We will cover the following:

* What is backpropagation?
* The chain rule of calculus
* Forward pass
* Loss calculation
* Backward pass (backpropagation)
* Step-by-step numeric example
* Weight update using gradient descent
* Backpropagation in Python

Let's get started: [Math Behind Backpropagation](https://outcomeschool.com/blog/math-behind-backpropagation)

---

## Math Behind Cross-Entropy Loss

In this blog, we will learn about the math behind Cross-Entropy Loss with a step-by-step numeric example.

When we train a classification model in machine learning, the model predicts probabilities for each class. For example, given an image, the model outputs something like: "I am 70% sure this is a cat, 20% sure it is a dog, and 10% sure it is a rabbit." To train the model, we need a way to measure how wrong these predictions are compared to the true answer. This is exactly what Cross-Entropy Loss does. It is the most widely used loss function in classification tasks, and it powers the training of almost every modern AI model, including GPT, BERT, and image classifiers.

We will cover the following:

* The Big Picture
* What is Cross-Entropy
* The Cross-Entropy Loss Formula
* Why We Take the Negative Log
* Binary Cross-Entropy Loss
* Categorical Cross-Entropy Loss
* Step-by-Step Numeric Example
* Cross-Entropy Loss for Language Models
* The Gradient of Cross-Entropy Loss
* Quick Summary

Let's get started: [Math Behind Cross-Entropy Loss](https://outcomeschool.com/blog/math-behind-cross-entropy-loss)

---

## Decoding Transformer Architecture

In this blog, we will learn about the Transformer architecture by decoding it piece by piece - understanding what each component does, how they work together, and why this architecture powers every modern Large Language Model (LLM).

We will cover the following:

* Why the Transformer was needed
* The two halves of the architecture
* Tokenization, Embedding, and Positional Encoding
* The Attention Mechanism and Multi-Head Attention
* Feed-Forward Networks, Residual Connections, and Layer Normalization
* How the Encoder and Decoder work
* How data flows through the entire architecture
* The three variants of the Transformer
* Why the Transformer is so powerful

Let's get started: [Decoding Transformer Architecture](https://outcomeschool.com/blog/decoding-transformer-architecture)

---

## Feed-Forward Networks in LLMs

In this blog, we will learn about Feed-Forward Networks in LLMs - understanding what they are, how they work inside the Transformer architecture, why every Transformer layer needs one, and what role they play in making Large Language Models so powerful.

We will cover the following:

* What is a Feed-Forward Network?
* Understanding Feed-Forward Networks with a Real-World Analogy
* Where Does the Feed-Forward Network Sit in a Transformer?
* How Does a Feed-Forward Network Work - Step by Step
* The Expand-then-Contract Pattern
* Why Does the FFN Expand and Then Contract?
* ReLU and Activation Functions
* What Does the Feed-Forward Network Actually Learn?
* How Much of the Model is the Feed-Forward Network?
* Feed-Forward Networks in Mixture of Experts
* Why Feed-Forward Networks Are So Important

Let's get started: [Feed-Forward Networks in LLMs](https://outcomeschool.com/blog/feed-forward-networks-in-llms)

---

## KV Cache in LLMs

In this blog, we will learn about KV Cache - where K stands for Key and V stands for Value - and why it is used in Large Language Models (LLMs) to speed up text generation.

We will start with how LLMs generate text one token at a time, understand the role of Key, Value, and Query inside the model, see the problem of repeated computation through an example, and then walk through how KV Cache solves this problem by storing and reusing past results.

We will cover the following:

* How LLMs Generate Text
* What Happens Inside the Model
* The Problem: Repeated Computation
* The Solution: KV Cache
* Why Only Key and Value Are Cached, Not Query
* How Much Faster Does It Get
* The Trade-Off: Speed vs Memory

Let's get started: [KV Cache in LLMs](https://outcomeschool.com/blog/kv-cache-in-llms)

---

## Paged Attention in LLMs

In this blog, we will learn about Paged Attention, a technique that solves the memory waste problem of KV Cache, allowing LLMs to serve many more users at the same time.

We will start with a quick recap of KV Cache, understand the memory problem it creates, see how traditional memory allocation wastes space through an example, and then walk through how Paged Attention solves this problem by borrowing an idea from how computers manage memory.

We will cover the following:

* Quick Recap: KV Cache
* The Problem: Memory Waste in KV Cache
* What is Paged Attention?
* How Paged Attention Works
* Why Paged Attention Is So Effective
* Memory Sharing Across Requests

Let's get started: [Paged Attention in LLMs](https://outcomeschool.com/blog/paged-attention-in-llms)

---

## Decoding Flash Attention in LLMs

In this blog, we will learn about Flash Attention by decoding it piece by piece - understanding why standard attention is slow, what makes Flash Attention fast, how it uses GPU memory cleverly, and why it is used in almost every modern Large Language Model (LLM).

We will cover the following:

* A quick recap of standard attention
* Why standard attention is slow
* How GPU memory actually works (HBM vs SRAM)
* The core idea behind Flash Attention
* Tiling: breaking the work into small blocks
* Online softmax: computing softmax without the full matrix
* Recomputation in the backward pass
* Flash Attention 2
* Flash Attention 3
* Advantages and impact of Flash Attention

Let's get started: [Decoding Flash Attention in LLMs](https://outcomeschool.com/blog/decoding-flash-attention)

---

## Mixture of Experts Explained

In this blog, we will learn about the Mixture of Experts (MoE) architecture - understanding what experts are, how the router picks them, why MoE makes large models faster and cheaper, and why it powers many of today's most powerful Large Language Models (LLMs).

We will cover the following:

* Why Mixture of Experts was needed
* What an "expert" really means
* The router and how it picks experts
* Where MoE sits inside a Transformer
* Sparse activation and why it saves compute
* Load balancing across experts
* Advantages and challenges of MoE
* Why MoE powers many modern LLMs

Let's get started: [Mixture of Experts Explained](https://outcomeschool.com/blog/mixture-of-experts)

---

## Harness Engineering in AI

In this blog, we will learn about Harness Engineering in AI. We will understand what a harness is, why we need it, and how it is used in AI Agents and evaluation systems.

We will cover the following:

* What is a Harness in AI?
* Why do we need Harness Engineering?
* Components of an AI Harness
* Harness Engineering for AI Agents
* Harness Engineering for Evaluation
* Best Practices in Harness Engineering
* Putting It All Together

Let's get started: [Harness Engineering in AI](https://outcomeschool.com/blog/harness-engineering-in-ai)

---

## More blogs and videos coming soon!

### License
```
   Copyright (C) 2026 Outcome School

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

## Recent Commits

- 2026-04-20 82141f0 AMIT SHEKHAR: Add section on Cross-Entropy Loss to README
- 2026-04-14 5f11e4a AMIT SHEKHAR: Update README.md
- 2026-04-13 8f3c019 AMIT SHEKHAR: Add section on Feed-Forward Networks in LLMs
- 2026-04-12 1bb5239 AMIT SHEKHAR: Update README.md
- 2026-04-12 a7d11e2 AMIT SHEKHAR: Initialize README with blog topics on AI
- 2026-04-12 22b6737 AMIT SHEKHAR: Add files via upload
- 2026-04-12 8284c47 AMIT SHEKHAR: Configure .gitattributes for Markdown files
- 2026-04-12 7e807b6 AMIT SHEKHAR: Add files via upload
- 2026-04-12 59096f5 AMIT SHEKHAR: Create banner.png
- 2026-04-12 5d7141f AMIT SHEKHAR: Initial commit


## File: LICENSE

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

```
<!-- fetched-content:end -->
