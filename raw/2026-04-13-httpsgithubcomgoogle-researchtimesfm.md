---
title: https://github.com/google-research/timesfm
type: url
captured: 2026-04-13 17:25:04.763317+00:00
source: android-share
url: https://github.com/google-research/timesfm
content_hash: sha256:af17780464736162d3eeb7fb035144dee603f89b6dce89d650ccc84d1410e8d7
tags: []
status: ingested
last_refreshed: '2026-04-22T02:45:09+00:00'
---

https://github.com/google-research/timesfm

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:45:09+00:00
- source_url: https://github.com/google-research/timesfm
- resolved_url: https://github.com/google-research/timesfm
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: google-research/timesfm
Description: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.
Stars: 18302
Language: Python

## README

# TimesFM

TimesFM (Time Series Foundation Model) is a pretrained time-series foundation
model developed by Google Research for time-series forecasting.

*   Paper:
    [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688),
    ICML 2024.
*   All checkpoints:
    [TimesFM Hugging Face Collection](https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6).
*   [Google Research blog](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/).
*   TimesFM in Google 1P Products:
    *   [BigQuery ML](https://cloud.google.com/bigquery/docs/timesfm-model): Enterprise level SQL queries for scalability and reliability.
    *   [Google Sheets](https://workspaceupdates.googleblog.com/2026/02/forecast-data-in-connected-sheets-BigQueryML-TimesFM.html): For your daily spreadsheet. 
    *   [Vertex Model Garden](https://pantheon.corp.google.com/vertex-ai/publishers/google/model-garden/timesfm): Dockerized endpoint for agentic calling.

This open version is not an officially supported Google product.

**Latest Model Version:** TimesFM 2.5

**Archived Model Versions:**

-   1.0 and 2.0: relevant code archived in the sub directory `v1`. You can `pip
    install timesfm==1.3.0` to install an older version of this package to load
    them.

## Update - Apr. 9, 2026

Added fine-tuning example using HuggingFace Transformers + PEFT (LoRA) — see
[`timesfm-forecasting/examples/finetuning/`](timesfm-forecasting/examples/finetuning/).
Also added unit tests (`tests/`) and incorporated several community fixes.

Shoutout to [@kashif](https://github.com/kashif) and [@darkpowerxo](https://github.com/darkpowerxo). 

## Update - Mar. 19, 2026

Huge shoutout to [@borealBytes](https://github.com/borealBytes) for adding the support for [AGENTS](https://github.com/google-research/timesfm/blob/master/AGENTS.md)! TimesFM [SKILL.md](https://github.com/google-research/timesfm/tree/master/timesfm-forecasting) is out.

## Update - Oct. 29, 2025

Added back the covariate support through XReg for TimesFM 2.5.


## Update - Sept. 15, 2025

TimesFM 2.5 is out!

Comparing to TimesFM 2.0, this new 2.5 model:

-   uses 200M parameters, down from 500M.
-   supports up to 16k context length, up from 2048.
-   supports continuous quantile forecast up to 1k horizon via an optional 30M
    quantile head.
-   gets rid of the `frequency` indicator.
-   has a couple of new forecasting flags.

Since the Sept. 2025 launch, the following improvements have been completed:

1.  ✅ Flax version of the model for faster inference.
2.  ✅ Covariate support via XReg (see Oct. 2025 update).
3.  ✅ Documentation, examples, and agent skill (see `timesfm-forecasting/`).
4.  ✅ Fine-tuning example with LoRA via HuggingFace Transformers + PEFT (see `timesfm-forecasting/examples/finetuning/`).
5.  ✅ Unit tests for core layers, configs, and utilities (see `tests/`).

### Install

1.  Clone the repository:
    ```shell
    git clone https://github.com/google-research/timesfm.git
    cd timesfm
    ```

2.  Create a virtual environment and install dependencies using `uv`:
    ```shell
    # Create a virtual environment
    uv venv
    
    # Activate the environment
    source .venv/bin/activate
    
    # Install the package in editable mode with torch
    uv pip install -e .[torch]
    # Or with flax
    uv pip install -e .[flax]
    # Or XReg is needed
    uv pip install -e .[xreg]
    ```

3. [Optional] Install your preferred `torch` / `jax` backend based on your OS and accelerators
(CPU, GPU, TPU or Apple Silicon).:

-   [Install PyTorch](https://pytorch.org/get-started/locally/).
-   [Install Jax](https://docs.jax.dev/en/latest/installation.html#installation)
    for Flax.

### Code Example

```python
import torch
import numpy as np
import timesfm

torch.set_float32_matmul_precision("high")

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")

model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)
point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[
        np.linspace(0, 1, 100),
        np.sin(np.linspace(0, 20, 67)),
    ],  # Two dummy inputs
)
point_forecast.shape  # (2, 12)
quantile_forecast.shape  # (2, 12, 10): mean, then 10th to 90th quantiles.
```

Languages: Python 70.6%, HTML 21.1%, Jupyter Notebook 8.0%, Shell 0.3%

## Recent Releases

### v1.2.6 (2024-12-31)

Changes:
----
1. Add support for TimesFM-2.0 models.
2. Set the median head as the default point forecaster.

PyPI Release:
----
v1.2.6: Support for TimesFM-2.0 models.
- Add hparam support for TimesFM-2.0 models.
- Some bug fixes in pytorch decoding.
- Right now we do not support cached decoding in both jax and pytorch.

Checkpoints:
----
The TimesFM-2.0 checkpoints are available on Hugging Face:
- https://huggingface.co/google/timesfm-2.0-500m-jax
- https://huggingface.co/google/timesfm-2.0-500m-pytorch

Full Changelog:
----
https://github.com/google-research/timesfm/commits/v1.2.6

### v1.2.1 (2024-10-18)

Changes:
----
- PyTorch support for TimesFM inference.

PyPI Release:
----

v1.2.1: Support separate dependencies for `pax` and `torch` versions of TimesFM:
  - `pip install timesfm[pax]` for the `pax` version and `jax` checkpoints.
  - `pip install timesfm[torch]` for the `torch` version and checkpoints.
  - See the updated [README](https://github.com/google-research/timesfm?tab=readme-ov-file#usage) for the usage.

Checkpoints:
----
The PyTorch checkpoint for the 200m model is available on Hugging Face:
- https://huggingface.co/google/timesfm-1.0-200m-pytorch

Full Changelog:
----
https://gi…

## Recent Commits

- 2026-04-15 d720daa Yichen Zhou: Update README.md
- 2026-04-15 eacf761 Yichen Zhou: Merge pull request #398 from darkpowerxo/feat/peft-finetuning-pipeline-2.5
- 2026-04-10 6ae67d4 darkpowerxo: revert: drop PR #393 (xreg batch behavior) and PR #390 (SKILL.md link) per maintainer feedback
- 2026-04-09 caddef1 darkpowerxo: refactor: replace custom PEFT pipeline with Transformers+PEFT example
- 2026-04-09 18d5eb2 darkpowerxo: fix: improve PEFT device consistency and XReg output slicing
- 2026-04-08 ad192b7 darkpowerxo: docs: update README — replace 'under construction' with completed status
- 2026-04-08 54f5405 darkpowerxo: docs: fix swapped xreg_mode descriptions and typo in error message
- 2026-04-08 13a8eb2 darkpowerxo: ci: upgrade GitHub Actions to v6
- 2026-04-08 30f28a1 darkpowerxo: fix: correct SKILL.md link in README
- 2026-04-08 1bb44d5 darkpowerxo: fix: respect batch_size in v1 data_loader when permute=False
- 2026-04-08 a63360a darkpowerxo: fix: per-input ridge regression to prevent data leakage in xreg
- 2026-04-08 c10494a darkpowerxo: test: add unit tests for configs, torch layers, utils, and base utils
- 2026-04-08 bc03b77 darkpowerxo: fix: correct 'complied' typo and replace print with logging
- 2026-04-08 b6ac2b3 darkpowerxo: docs: add README for the PEFT fine-tuning pipeline
- 2026-04-08 a67eeb2 darkpowerxo: feat: add CLI entry-point and launch script for PEFT fine-tuning
- 2026-04-08 eca7ca3 darkpowerxo: feat: add multi-GPU PEFT trainer for TimesFM 2.5
- 2026-04-08 9875d92 darkpowerxo: feat: add TimeSeriesDataset for PEFT fine-tuning
- 2026-04-08 7357458 darkpowerxo: feat: add LoRA/DoRA adapter layers for TimesFM 2.5 (PyTorch)
- 2026-04-08 aa2b17f darkpowerxo: chore: update .gitignore for egg-info, uv.lock, peft_checkpoints
- 2026-04-03 f085b90 Yichen Zhou: Update README.md

## Recently Merged PRs (top 10)

- #398 feat: PEFT fine-tuning pipeline (LoRA/DoRA, multi-GPU) for TimesFM 2.5 (merged 2026-04-15)
- #376 docs: fix swapped xreg_mode descriptions in forecast_with_covariates (merged 2026-03-19)
- #369 feat(skill): ship first-party timesfm-forecasting Agent Skill (agentskills.io) (merged 2026-03-19)
- #372 [HF] use the ModelHubMixin api (merged 2026-03-11)
- #341 [TimesFMv1] fix variance calculation (merged 2026-02-19)
- #360 Update pyproject.toml (merged 2026-01-27)


## File: .gitignore

```
.venv/
dist/
__pycache__/
*.egg-info/
checkpoints/
wandb/
datasets/
results/
uv.lock
development_setup.md
debug.log

```


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


## File: pyproject.toml

```
[project]
name = "timesfm"
version = "2.0.0"
description = "A time series foundation model."
authors = [
    {name = "Rajat Sen", email = "senrajat@google.com"},
    {name = "Yichen Zhou", email = "yichenzhou@google.com"},
    {name = "Abhimanyu Das", email = "abhidas@google.com"},
    {name = "Petros Mol", email = "pmol@google.com"},
    {name = "Michael Chertushkin", email = "chertushkinmichael@gmail.com"},
]
license = {text = "Apache-2.0"}
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26.4",
    "huggingface_hub[cli]>=0.23.0",
    "safetensors>=0.5.3",
]

[project.optional-dependencies]
torch = [
    "torch>=2.0.0",
]
flax = [
    "flax",
    "optax",
    "einshape",
    "orbax-checkpoint",
    "jaxtyping",
    "jax[cuda]"
]
xreg = [
    "jax[cuda]",
    "scikit-learn",
]

[tool.ruff]
line-length = 88
indent-width = 2

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"


```


## File: requirements.txt

```
# This file was autogenerated by uv via the following command:
#    uv pip compile pyproject.toml -o requirements.txt
anyio==4.11.0
    # via httpx
certifi==2025.10.5
    # via
    #   httpcore
    #   httpx
click==8.3.0
    # via typer-slim
filelock==3.19.1
    # via huggingface-hub
fsspec==2025.9.0
    # via huggingface-hub
h11==0.16.0
    # via httpcore
hf-xet==1.2.0
    # via huggingface-hub
httpcore==1.0.9
    # via httpx
httpx==0.28.1
    # via huggingface-hub
huggingface-hub==1.0.1
    # via timesfm (pyproject.toml)
idna==3.10
    # via
    #   anyio
    #   httpx
numpy==2.2.6
    # via timesfm (pyproject.toml)
packaging==25.0
    # via huggingface-hub
pyyaml==6.0.3
    # via huggingface-hub
safetensors==0.6.2
    # via timesfm (pyproject.toml)
shellingham==1.5.4
    # via huggingface-hub
sniffio==1.3.1
    # via anyio
tqdm==4.67.1
    # via huggingface-hub
typer-slim==0.20.0
    # via huggingface-hub
typing-extensions==4.15.0
    # via
    #   anyio
    #   huggingface-hub
    #   typer-slim

```


## File: timesfm-forecasting/examples/finetuning/README.md

```
# Fine-Tuning TimesFM 2.5 with LoRA

Parameter-efficient fine-tuning of
[TimesFM 2.5](https://huggingface.co/google/timesfm-2.5-200m-transformers)
using **HuggingFace Transformers** and **PEFT (LoRA)**.

This approach is based on the fine-tuning workflow by
[@kashif](https://github.com/kashif) at HuggingFace
([notebook](https://github.com/huggingface/notebooks/blob/main/examples/timesfm2_5.ipynb)).

## How It Works

TimesFM 2.5 is available as a standard
[Transformers](https://github.com/huggingface/transformers) model
(`TimesFm2_5ModelForPrediction`). This means it supports the full Transformers
ecosystem out of the box, including:

- **PEFT adapters** — LoRA, QLoRA, etc. via the
  [`peft`](https://github.com/huggingface/peft) library
- **All attention backends** — eager, SDPA, Flash Attention 2/3, Flex Attention
- **Standard `from_pretrained` / `save_pretrained` workflow**

The model's forward pass natively computes a training loss when `future_values`
are provided, so fine-tuning requires nothing more than a standard PyTorch
training loop.

## Quick Start

### Install

```bash
pip install transformers accelerate peft pandas pyarrow scikit-learn
```

### Train

```bash
# Fine-tune with default settings on the retail sales dataset
python finetune_lora.py

# Custom hyperparameters
python finetune_lora.py \
    --epochs 20 \
    --batch_size 64 \
    --lr 5e-5 \
    --lora_r 8 \
    --lora_alpha 16 \
    --context_len 64 \
    --horizon_len 13 \
    --output_dir my-retail-adapter
```

### Evaluate

```bash
# Evaluate a previously trained adapter (skip training)
python finetune_lora.py --eval_only --output_dir timesfm2_5-retail-lora
```

## Key Concepts

### No External Normalisation

TimesFM 2.5 applies its own internal instance normalisation (RevIN). **Do not**
normalise your data externally — feed raw values and let the model handle it.

### Random Window Sampling

Following [Chronos-2](https://github.com/amazon-science/chronos-forecasting),
each training example is a random `(context, horizon)` window sliced from one of
the input series. This is more data-efficient than always using the same
fixed window per series.

### LoRA Target Modules

Using `target_modules="all-linear"` applies LoRA to every linear layer in the
model. With `r=4` this adds only ~0.6% trainable parameters (~1.4M out of
~232M), which is enough to meaningfully adapt the model to a new domain.

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--model_id` | `google/timesfm-2.5-200m-transformers` | HuggingFace model ID |
| `--context_len` | `64` | Context length for training windows |
| `--horizon_len` | `13` | Forecast horizon in time steps |
| `--epochs` | `10` | Training epochs |
| `--batch_size` | `32` | Batch size |
| `--lr` | `1e-4` | Learning rate |
| `--lora_r` | `4` | LoRA rank |
| `--lora_alpha` | `8` | LoRA alpha |
| `--lora_dropout` | `0.05` | LoRA dropout |
| `--num_samples` | `5000` | Random training windows to pre-sample |
| `--output_dir` | `timesfm2_5-retail-lora` | Where to save the adapter |
| `--seed` | `42` | Random seed |
| `--eval_only` | — | Skip training; evaluate existing adapter |

## Acknowledgements

The Transformers integration and fine-tuning approach were developed by
[@kashif](https://github.com/kashif) at HuggingFace. See the original notebook:
<https://github.com/huggingface/notebooks/blob/main/examples/timesfm2_5.ipynb>

```


## File: timesfm-forecasting/examples/global-temperature/README.md

```
# TimesFM Forecast Report: Global Temperature Anomaly (2025)

**Model:** TimesFM 1.0 (200M) PyTorch  
**Generated:** 2026-02-21  
**Source:** NOAA GISTEMP Global Land-Ocean Temperature Index

---

## Executive Summary

TimesFM forecasts a mean temperature anomaly of **1.19°C** for 2025, slightly below the 2024 average of 1.25°C. The model predicts continued elevated temperatures with a peak of 1.30°C in March 2025 and a minimum of 1.06°C in December 2025.

---

## Input Data

### Historical Temperature Anomalies (2022-2024)

| Date | Anomaly (°C) | Date | Anomaly (°C) | Date | Anomaly (°C) |
|------|-------------|------|-------------|------|-------------|
| 2022-01 | 0.89 | 2023-01 | 0.87 | 2024-01 | 1.22 |
| 2022-02 | 0.89 | 2023-02 | 0.98 | 2024-02 | 1.35 |
| 2022-03 | 1.02 | 2023-03 | 1.21 | 2024-03 | 1.34 |
| 2022-04 | 0.88 | 2023-04 | 1.00 | 2024-04 | 1.26 |
| 2022-05 | 0.85 | 2023-05 | 0.94 | 2024-05 | 1.15 |
| 2022-06 | 0.88 | 2023-06 | 1.08 | 2024-06 | 1.20 |
| 2022-07 | 0.88 | 2023-07 | 1.18 | 2024-07 | 1.24 |
| 2022-08 | 0.90 | 2023-08 | 1.24 | 2024-08 | 1.30 |
| 2022-09 | 0.88 | 2023-09 | 1.47 | 2024-09 | 1.28 |
| 2022-10 | 0.95 | 2023-10 | 1.32 | 2024-10 | 1.27 |
| 2022-11 | 0.77 | 2023-11 | 1.18 | 2024-11 | 1.22 |
| 2022-12 | 0.78 | 2023-12 | 1.16 | 2024-12 | 1.20 |

**Statistics:**
- Total observations: 36 months
- Mean anomaly: 1.09°C
- Trend (2022→2024): +0.37°C

---

## Raw Forecast Output

### Point Forecast and Confidence Intervals

| Month | Point | 80% CI | 90% CI |
|-------|-------|--------|--------|
| 2025-01 | 1.259 | [1.141, 1.297] | [1.248, 1.324] |
| 2025-02 | 1.286 | [1.141, 1.340] | [1.277, 1.375] |
| 2025-03 | 1.295 | [1.127, 1.355] | [1.287, 1.404] |
| 2025-04 | 1.221 | [1.035, 1.290] | [1.208, 1.331] |
| 2025-05 | 1.170 | [0.969, 1.239] | [1.153, 1.289] |
| 2025-06 | 1.146 | [0.942, 1.218] | [1.128, 1.270] |
| 2025-07 | 1.170 | [0.950, 1.248] | [1.151, 1.300] |
| 2025-08 | 1.203 | [0.971, 1.284] | [1.186, 1.341] |
| 2025-09 | 1.191 | [0.959, 1.283] | [1.178, 1.335] |
| 2025-10 | 1.149 | [0.908, 1.240] | [1.126, 1.287] |
| 2025-11 | 1.080 | [0.836, 1.176] | [1.062, 1.228] |
| 2025-12 | 1.061 | [0.802, 1.153] | [1.037, 1.217] |

### JSON Output

```json
{
  "model": "TimesFM 1.0 (200M) PyTorch",
  "input": {
    "source": "NOAA GISTEMP Global Temperature Anomaly",
    "n_observations": 36,
    "date_range": "2022-01 to 2024-12",
    "mean_anomaly_c": 1.089
  },
  "forecast": {
    "horizon": 12,
    "dates": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
              "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"],
    "point": [1.259, 1.286, 1.295, 1.221, 1.170, 1.146, 1.170, 1.203, 1.191, 1.149, 1.080, 1.061]
  },
  "summary": {
    "forecast_mean_c": 1.186,
    "forecast_max_c": 1.295,
    "forecast_min_c": 1.061,
    "vs_last_year_mean": -0.067
  }
}
```

---

## Visualization

![Temperature Anomaly Forecast](forecast_visualization.png)

---

## Findings

### Key Observations

1. **Slight cooling trend expected**: The model forecasts a mean anomaly 0.07°C below 2024 levels, suggesting a potential stabilization after the record-breaking temperatures of 2023-2024.

2. **Seasonal pattern preserved**: The forecast shows the expected seasonal variation with higher anomalies in late winter (Feb-Mar) and lower in late fall (Nov-Dec).

3. **Widening uncertainty**: The 90% CI expands from ±0.04°C in January to ±0.08°C in December, reflecting typical forecast uncertainty growth over time.

4. **Peak temperature**: March 2025 is predicted to have the highest anomaly at 1.30°C, potentially approaching the September 2023 record of 1.47°C.

### Limitations

- TimesFM is a zero-shot forecaster without physical climate model constraints
- The 36-month training window may not capture multi-decadal climate trends
- El Niño/La Niña cycles are not explicitly modeled

### Recommendations

- Use this forecast as a baseline comparison for physics-based climate models
- Update forecast quarterly as new observations become available
- Consider ensemble approaches combining TimesFM with other methods

---

## Reproducibility

### Files

| File | Description |
|------|-------------|
| `temperature_anomaly.csv` | Input data (36 months) |
| `forecast_output.csv` | Point forecast with quantiles |
| `forecast_output.json` | Machine-readable forecast |
| `forecast_visualization.png` | Fan chart visualization |
| `run_forecast.py` | Forecasting script |
| `visualize_forecast.py` | Visualization script |
| `run_example.sh` | One-click runner |

### How to Reproduce

```bash
# Install dependencies
uv pip install "timesfm[torch]" matplotlib pandas numpy

# Run the complete example
cd scientific-skills/timesfm-forecasting/examples/global-temperature
./run_example.sh
```

---

## Technical Notes

### API Discovery

The TimesFM PyTorch API differs from the GitHub README documentation:

**Documented (GitHub README):**
```python
model = timesfm.TimesFm(
    context_len=512,
    horizon_len=128,
    backend="gpu",
)
model.load_from_google_repo("google/timesfm-2.5-200m-pytorch")
```

**Actual Working API:**
```python
hparams = timesfm.TimesFmHparams(horizon_len=12)
checkpoint = timesfm.TimesFmCheckpoint(
    huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
)
model = timesfm.TimesFm(hparams=hparams, checkpoint=checkpoint)
```

### TimesFM 2.5 PyTorch Issue

The `google/timesfm-2.5-200m-pytorch` checkpoint downloads as `model.safetensors`, but the TimesFM loader expects `torch_model.ckpt`. This causes a `FileNotFoundError` at model load time. Using TimesFM 1.0 PyTorch resolves this issue.

---

*Report generated by TimesFM Forecasting Skill (claude-scientific-skills)*

```


## File: v1/experiments/extended_benchmarks/README.md

```
# Extended Benchmarks

The benchmark setting has been borrowed from Nixtla's original [benchmarking](https://github.com/AzulGarza/nixtla/tree/main/experiments/amazon-chronos) of time-series foundation models against a strong statistical ensemble. Later more datasets were added by the Chronos team in this [pull request](https://github.com/shchur/nixtla/tree/chronos-full-eval/experiments/amazon-chronos). We compare on all the datasets in this extended benchmarks.


## Running TimesFM on the benchmark

We need to add the following packages for running these benchmarks. Follow the installation instructions till before `poetry lock`. Then,

```
poetry add git+https://github.com/awslabs/gluon-ts.git
poetry lock
poetry install --only <pax or pytorch>
```

To run the timesfm on the benchmark do:

```
poetry run python3 -m experiments.extended_benchmarks.run_timesfm --model_path=google/timesfm-1.0-200m(-pytorch) --backend="gpu"
```


Note: In the current version of TimesFM we focus on point forecasts and therefore the mase, smape have been calculated using the quantile head corresponding to the median i.e 0.5 quantile. We do offer 10 quantile heads but they have not been calibrated after pretraining. We recommend using them with caution or calibrate/conformalize them on a hold out for your applications. More to follow on later versions.

## Benchmark Results for TimesFM-1.0

![Benchmark Results Table](./tfm_extended_new.png)

__Update:__ We have added TimeGPT-1 to the benchmark results. We had to remove the Dominick dataset as we were not able to run TimeGPT-1 on this benchmark. Note that the previous results including Dominick remain available at `./tfm_results.png`. In order to reproduce the results for TimeGPT-1, please run `run_timegpt.py`.

_Remark:_ All baselines except the ones involving TimeGPT were run performed on a [g2-standard-32](https://cloud.google.com/compute/docs/gpus). Since TimeGPT-1 can only be accessed by an API, the time column might not reflect the true speed of the model as it also includes the communication cost. Moreover, we are not sure about the exact backend hardware for TimeGPT. The TimesFM latency numbers are from the PAX version.

We can see that TimesFM performs the best in terms of both mase and smape. More importantly it is much faster than the other methods, in particular it is more than 600x faster than StatisticalEnsemble and 80x faster than Chronos (Large).

Note: This benchmark only compares on `one` small horizon window for long horizon datasets like ETT hourly and 15 minutes. More in depth comparison on longer horizon rolling validation tasks are presented in our long horizon benchmarks.
```


## File: v1/experiments/long_horizon_benchmarks/README.md

```
# Extended Benchmarks

We benchmark on the original test set for ETT datasets as per long horizon benchmark papers (see [here](https://openreview.net/forum?id=pCbC3aQB5W) for example.) In the original benchmark, rolling validation task on all test windows (with a stride of 1) is considered. While we can easily run our method on this task, the baselines can take a very long time to run. Therefore we present results on a modified task with stride between windows set to Horizon length i.e all disjoint horizons in the test period is considered.

All experiments were performed on a [g2-standard-32](https://cloud.google.com/compute/docs/gpus). We compare TimesFM with [Amazon-Chronos](https://github.com/amazon-science/chronos-forecasting).

## Running TimesFM on the benchmark

We need to add the following packages for running these benchmarks. Follow the installation instructions till before `poetry lock`. Then,

```
poetry add git+https://github.com/awslabs/gluon-ts.git
poetry add git+https://github.com/amazon-science/chronos-forecasting.git
poetry lock
poetry install --only pax
```
Note that for now only the pax version runs on this benchmark, because we had to remove the old tf dependency from the pytorch version. We will fix this issue soon.

To run the timesfm on the benchmark do:

```
poetry run python3 -m experiments.long_horizon_benchmarks.run_eval \
--model_path=google/timesfm-1.0-200m --backend="gpu" \
--pred_len=96 --context_len=512 --dataset=etth1
```

In the above, `<model_path>` should point to the checkpoint directory that can be downloaded from HuggingFace. 

For running chronos on the same benchmark you can run the command,

```
poetry run python3 -m experiments.long_horizon_benchmarks.run_eval \
--model_path=amazon/chronos-t5-mini --backend="gpu" \
--pred_len=96 --context_len=512 --dataset=etth1
```

You can change the model size from "mini" to "large" as required. The datasets we benchmark on are etth1, etth2, ettm1 and ettm2.

## Benchmark Results for TimesFM-1.0

![Benchmark Results Table](./tfm_long_horizon.png)

We compare the performance on horizon lengths of 96, 192 and 336, while context length is held fixed at 512.

We can see that TimesFM performs the best in terms of both wape and smape. More importantly it is much faster than the other methods, in particular it is more than 1000x faster than Chronos (Large).
```


## File: v1/LICENSE

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


## File: v1/peft/README.md

```
# Fine-Tuning Pipeline

This folder contains a generic fine-tuning pipeline designed to support multiple PEFT fine-tuning strategies.

## Features

- **Supported Fine-Tuning Strategies**:
  - **Full Fine-Tuning**: Adjusts all parameters of the model during training.
  - **[Linear Probing](https://arxiv.org/abs/2302.11939)**: Fine-tunes only the residual blocks and the embedding layer, leaving other parameters unchanged.
  - **[LoRA (Low-Rank Adaptation)](https://arxiv.org/abs/2106.09685)**: A memory-efficient method that fine-tunes a small number of parameters by decomposing the weight matrices into low-rank matrices.
  - **[DoRA (Directional LoRA)](https://arxiv.org/abs/2402.09353v4)**: An extension of LoRA that decomposes pre-trained weights into magnitude and direction components. It uses LoRA for directional adaptation, enhancing learning capacity and stability without additional inference overhead.

## Usage
### Fine-Tuning Script
The provided finetune.py script allows you to fine-tune a model with specific configurations. You can customize various parameters to suit your dataset and desired fine-tuning strategy.

Example Usage:

```zsh
source finetune.sh
```
This script runs the finetune.py file with a predefined set of hyperparameters for the model. You can adjust the parameters in the script as needed.

### Available Options
Run the script with the --help flag to see a full list of available options and their descriptions:
```zsh
python3 finetune.py --help
```
Script Configuration
You can modify the following key parameters directly in the finetune.sh script:
Fine-Tuning Strategy: Toggle between full fine-tuning, LoRA \[`--use-lora`\], DoRA [\[`--use-dora`\]], or Linear Probing \[`--use-linear-probing`\].

### Performance Comparison
The figure below compares the performance of LoRA/DoRA against Linear Probing under the following conditions:

<img width="528" alt="image" src="https://github.com/user-attachments/assets/6c9f820b-5865-4821-8014-c346b9d632a5">

- Training data split: 60% train, 20% validation, 20% test.
- Benchmark: context_len=128, horizon_len=96
- Fine-tuning: context_len=128, horizon_len=128
- Black: Best result.
- Blue: Second best result.

```


## File: v1/pyproject.toml

```
[tool.poetry]
name = "timesfm"
packages = [
    { include = "timesfm", from = "src" },
    { include = "finetuning", from = "src" },
]
description = "Open weights time-series foundation model from Google Research."
version = "1.3.0"
authors = [
    "Rajat Sen <senrajat@google.com>",
    "Yichen Zhou <yichenzhou@google.com>",
    "Abhimanyu Das <abhidas@google.com>",
    "Petros Mol <pmol@google.com>",
    "Justin Güse <guese.justin@gmail.com>",
    "Michael Chertushkin <chertushkinmichael@gmail.com>"
]
readme = "README.md"
keywords = ["time series", "timesfm", "forecast", "time series model"]
homepage = "https://github.com/google-research/timesfm"
repository = "https://github.com/google-research/timesfm"
classifiers = [
    "Environment :: Console",
    "Framework :: Flake8",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
]
include = ["LICENSE"]

[tool.poetry.dependencies]
python = ">=3.10,<3.12"
einshape = ">=1.0.0"
numpy = ">=1.26.4"
pandas = ">=2.0.0"
utilsforecast = ">=0.1.10"
huggingface_hub = { version = ">=0.23.0", extras = ["cli"] }
scikit-learn = ">=1.2.2"
typer = ">=0.12.3"
wandb = ">=0.17.5"
absl-py = ">=1.4.0"
safetensors = "^0.5.3"

[tool.poetry.extras]
# Note: `lingvo` is an optional Google-internal dependency with strict Python
# version and packaging constraints that cause install failures on some
# environments (Colab etc.). We omit it from the pax extra here so users can
# opt-in explicitly if they need it and have a compatible environment.
pax = ["paxml", "jax", "jaxlib"]
torch = ["torch"] 

[tool.poetry.dependencies.paxml]
version = ">=1.4.0"
python = ">=3.10,<3.11"



[tool.poetry.dependencies.jax]
version = ">=0.4.26"
extras = ["cuda12"]
python = ">=3.10,<3.12"  # Support both python versions

[tool.poetry.dependencies.jaxlib]
version = ">=0.4.26"
python = ">=3.10,<3.12"  # Support both python versions

[tool.poetry.dependencies.torch]
version = ">=2.0.0"
extras = ["cuda"]
python = ">=3.11,<3.12"

[tool.poetry.group.dev.dependencies]
pytest = ">=8.3.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

```


## File: v1/README.md

```
# TimesFM

TimesFM  (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google
Research for time-series forecasting.

* Paper: [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688), to appear in ICML 2024.
* [Google Research blog](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/)
* [Hugging Face release](https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6)

This repo contains the code to load public TimesFM checkpoints and run model
inference. Please visit our 
[Hugging Face release](https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6)
to download model checkpoints.

This is not an officially supported Google product.

We recommend at least 32GB RAM to load TimesFM dependencies.

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common installation and usage issues.

## Update - Dec. 30, 2024
- We are launching a 500m checkpoint as a part of TimesFM-2.0 release. This new checkpoint can be upto 25% better than v1.0 on leading benchmarks and also has a 4 times longer max. context length.
- Launched [finetuning support](https://github.com/google-research/timesfm/blob/master/notebooks/finetuning.ipynb) that lets you finetune the weights of the pretrained TimesFM model on your own data.
- Launched [~zero-shot covariate support](https://github.com/google-research/timesfm/blob/master/notebooks/covariates.ipynb) with external regressors. More details [here](https://github.com/google-research/timesfm?tab=readme-ov-file#covariates-support).

## Update - Feb. 17, 2024
- We are providing the option for [finetuning using Pytorch](https://github.com/google-research/timesfm/blob/master/notebooks/finetuning_torch.ipynb), which mimics the previously added functionality from [finetuning support](https://github.com/google-research/timesfm/blob/master/notebooks/finetuning.ipynb).
- We are also providing the Multi-GPU finetuining with Pytorch. We currently support DDP multi-gpu finetuning, other variants of multi-gpu training (pipeline parallelism/model parallelism) might be added later. In order to use it, follow the steps in [finetuning example](https://github.com/google-research/timesfm/blob/master/finetuning/finetuning_example.py) .

## Checkpoint timesfm-1.0-200m (-pytorch)

timesfm-1.0-200m is our first open model checkpoint:

- It performs univariate time series forecasting for context lengths up to 512 timepoints and any horizon lengths, with an optional frequency indicator.
- It focuses on point forecasts, and does not support probabilistic forecasts. We experimentally offer quantile heads but they have not been calibrated after pretraining.

## Checkpoint timesfm-2.0-500m (-jax/-pytorch)

timesfm-2.0-500m is our second open model checkpoint:

- It performs univariate time series forecasting for context lengths up to 2048 timepoints and any horizon lengths, with an optional frequency indicator.
- It focuses on point forecasts. We experimentally offer 10 quantile heads but they have not been calibrated after pretraining.
- This new checkpoint can be upto 25% better than v1.0 on leading benchmarks and also has a 4 times longer max. context length.

## Benchmarking

TimesFM 2.0 has been added to [GIFT-Eval](https://huggingface.co/spaces/Salesforce/GIFT-Eval) which is one of the most comprehensive time-series bechmarks available. It takes the top spot in terms of aggregated MASE and CRPS, where it is 6\% better than the next best model in terms of aggregated MASE.

## Installation

### Local installation using poetry

We will be using `pyenv` and `poetry`. In order to set these things up please follow the instructions [here](https://substack.com/home/post/p-148747960?r=28a5lx&utm_campaign=post&utm_medium=web). Note that the PAX (or JAX) version needs to run on python 3.10.x and the PyTorch version can run on >=3.11.x. Therefore make sure you have two versions of python installed:

```
pyenv install 3.10
pyenv install 3.11
pyenv versions # to list the versions available (lets assume the versions are 3.10.15 and 3.11.10)
```

### For PAX version installation do the following.

```
pyenv local 3.10.15
poetry env use 3.10.15
poetry lock
poetry install -E  pax
```

After than you can run the timesfm under `poetry shell` or do `poetry run python3 ...`.

### For PyTorch version installation do the following.

```
pyenv local 3.11.10
poetry env use 3.11.10
poetry lock
poetry install -E  torch
```

After than you can run the timesfm under `poetry shell` or do `poetry run python3 ...`.

**Additional Note**: 

If you plan to use the **`forecast_with_covariates`** function (which requires external regressors), 
you need to install **JAX** and **jaxlib**. If you installed the base version of TimesFM (`torch`), you must manually install the dependencies for **`forecast_with_covariates`** support:
```
pip install jax jaxlib
```

**Why is this needed?**  
The `forecast_with_covariates` method relies on the `xreg_lib` module, which depends on JAX and jaxlib. If these packages are not installed, 
calling `forecast_with_covariates` will raise an error. However, due to a lazy import mechanism, `xreg_lib` (and hence JAX/jaxlib) is not needed for standard `forecast` calls.

### Notes

1. Running the provided benchmarks would require additional dependencies. Please see the `experiments` folder.

2. The dependency `lingvo` does not support ARM architectures, and the code is not working for machines with Apple silicon. We are aware of this issue and are working on a solution. Stay tuned.

### Install from PyPI (and publish)

On python 3.11 you can install the torch version using:

```pip install timesfm[torch]```

On python 3.10 you can install the pax version using:

```pip install timesfm[pax]```


## Usage 

### Initialize the model and load a checkpoint.
Then the base class can be loaded as,

```python
import timesfm

# Loading the timesfm-2.0 checkpoint:
# For PAX
tfm = timesfm.TimesFm(
      hparams=timesfm.TimesFmHparams(
          backend="gpu",
          per_core_batch_size=32,
          horizon_len=128,
          num_layers=50,
          context_len=2048,

          use_positional_embedding=False,
      ),
      checkpoint=timesfm.TimesFmCheckpoint(
          huggingface_repo_id="google/timesfm-2.0-500m-jax"),
  )

# For Torch
tfm = timesfm.TimesFm(
      hparams=timesfm.TimesFmHparams(
          backend="gpu",
          per_core_batch_size=32,
          horizon_len=128,
          num_layers=50,
          use_positional_embedding=False,
          context_len=2048,
      ),
      checkpoint=timesfm.TimesFmCheckpoint(
          huggingface_repo_id="google/timesfm-2.0-500m-pytorch"),
  )

# Loading the timesfm-1.0 checkpoint:
# For PAX
tfm = timesfm.TimesFm(
      hparams=timesfm.TimesFmHparams(
          backend="gpu",
          per_core_batch_size=32,
          horizon_len=128,
      ),
      checkpoint=timesfm.TimesFmCheckpoint(
          huggingface_repo_id="google/timesfm-1.0-200m"),
  )

# For Torch
tfm = timesfm.TimesFm(
      hparams=timesfm.TimesFmHparams(
          backend="gpu",
          per_core_batch_size=32,
          horizon_len=128,
      ),
      checkpoint=timesfm.TimesFmCheckpoint(
          huggingface_repo_id="google/timesfm-1.0-200m-pytorch"),
  )
```

Note some of the parameters are fixed to load the 200m and 500m models

1. The `context_len` in `hparams` here can be set as the max context length **of the model** (a maximum of 2048 for 2.0 models and 512 for 1.0 models). **It needs to be a multiplier of `input_patch_len`, i.e. a multiplier of 32.** You can provide a shorter series to the `tfm.forecast()` function and the model will handle it. The input time series can have **any context length**. Padding / truncation will be handled by the inference code if needed.

2. The horizon length can be set to anything. We recommend setting it to the largest horizon length you would need in the forecasting tasks for your application. We generally recommend horizon length <= context length but it is not a requirement in the function call.

3. `backend` is one of "cpu", "gpu", case sensitive.

### Perform inference

We provide APIs to forecast from either array inputs or `pandas` dataframe. Both forecast methods expect (1) the input time series contexts, (2) along with their frequencies. Please look at the documentation of the functions `tfm.forecast()` and `tfm.forecast_on_df()` for detailed instructions.

In particular regarding the frequency, TimesFM expects a categorical indicator valued in {0, 1, 2}:

- **0** (default): high frequency, long horizon time series. We recommend using this for time series up to daily granularity.
- **1**: medium frequency time series. We recommend using this for weekly and monthly data.
- **2**: low frequency, short horizon time series. We recommend using this for anything beyond monthly, e.g. quarterly or yearly.

This categorical value should be directly provided with the array inputs. For dataframe inputs, we convert the conventional letter coding of frequencies to our expected categories, that

- **0**: T, MIN, H, D, B, U
- **1**: W, M
- **2**: Q, Y

Notice you do **NOT** have to strictly follow our recommendation here. Although this is our setup during model training and we expect it to offer the best forecast result, you can also view the frequency input as a free parameter and modify it per your specific use case.


Examples:

Array inputs, with the frequencies set to low, medium and high respectively.

```python
import numpy as np
forecast_input = [
    np.sin(np.linspace(0, 20, 100)),
    np.sin(np.linspace(0, 20, 200)),
    np.sin(np.linspace(0, 20, 400)),
]
frequency_input = [0, 1, 2]

point_forecast, experimental_quantile_forecast = tfm.forecast(
    forecast_input,
    freq=frequency_input,
)
```

`pandas` dataframe, with the frequency set to "M" monthly.

```python
import pandas as pd

# e.g. input_df is
#       unique_id  ds          y
# 0     T1         1975-12-31  697458.0
# 1     T1         1976-01-31  1187650.0
# 2     T1         1976-02-29  1069690.0
# 3     T1         1976-03-31  1078430.0
# 4     T1         1976-04-30  1059910.0
# ...   ...        ...         ...
# 8175  T99        1986-01-31  602.0
# 8176  T99        1986-02-28  684.0
# 8177  T99        1986-03-31  818.0
# 8178  T99        1986-04-30  836.0
# 8179  T99        1986-05-31  878.0

forecast_df = tfm.forecast_on_df(
    inputs=input_df,
    freq="M",  # monthly
    value_name="y",
    num_jobs=-1,
)
```

## Covariates Support

We now have an external regressors library on top of TimesFM that can support static covariates as well as dynamic covariates available in the future. We have an usage example in [notebooks/covariates.ipynb](https://github.com/google-research/timesfm/blob/master/notebooks/covariates.ipynb).

If you plan to use the **`forecast_with_covariates`** on timesfm `torch` version, you need to install **JAX** and **jaxlib**. 
You must manually install the dependencies for **`forecast_with_covariates`** support:
```
pip install jax jaxlib
```

Let's take a toy example of forecasting sales for a grocery store: 

**Task:** Given the observed the daily sales of this week (7 days), forecast the daily sales of next week (7 days).

```
Product: ice cream
Daily_sales: [30, 30, 4, 5, 7, 8, 10]
Category: food
Base_price: 1.99
Weekday: [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6]
Has_promotion: [Yes, Yes, No, No, No, Yes, Yes, No, No, No, No, No, No, No]
Daily_temperature: [31.0, 24.3, 19.4, 26.2, 24.6, 30.0, 31.1, 32.4, 30.9, 26.0, 25.0, 27.8, 29.5, 31.2]
```

```
Product: sunscreen
Daily_sales: [5, 7, 12, 13, 5, 6, 10]
Category: skin product
Base_price: 29.99
Weekday: [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6]
Has_promotion: [No, No, Yes, Yes, No, No, No, Yes, Yes, Yes, Yes, Yes, Yes, Yes]
Daily_temperature: [31.0, 24.3, 19.4, 26.2, 24.6, 30.0, 31.1, 32.4, 30.9, 26.0, 25.0, 27.8, 29.5, 31.2]
```

In this example, besides the `Daily_sales`, we also have covariates `Category`, `Base_price`, `Weekday`, `Has_promotion`, `Daily_temperature`. Let's introduce some concepts:

**Static covariates** are covariates for each time series. 
- In our example, `Category` is a **static categorical covariate**, 
- `Base_price` is a **static numerical covariates**.

**Dynamic covariates** are covaraites for each time stamps.
- Date / time related features can be usually treated as dynamic covariates.
- In our example, `Weekday` and `Has_promotion` are **dynamic categorical covariates**.
- `Daily_temperate` is a **dynamic numerical covariate**.

**Notice:** Here we make it mandatory that the dynamic covariates need to cover both the forecasting context and horizon. For example, all dynamic covariates in the example have 14 values: the first 7 correspond to the observed 7 days, and the last 7 correspond to the next 7 days.

We can now provide the past data of the two products along with static and dynamic covariates as a batch input to TimesFM and produce forecasts that take into the account the covariates. To learn more, check out the example in [notebooks/covariates.ipynb](https://github.com/google-research/timesfm/blob/master/notebooks/covariates.ipynb).

## Finetuning

We have provided an example of finetuning the model on a new dataset in [notebooks/finetuning.ipynb](https://github.com/google-research/timesfm/blob/master/notebooks/finetuning.ipynb).

## Contribution Style guide

If you would like to submit a PR please make sure that you use our formatting style. We use [yapf](https://github.com/google/yapf) for formatting with the following options,

```
[style]
based_on_style = google
# Add your custom style rules here
indent_width = 2
spaces_before_comment = 2

```

Please run `yapf --in-place --recursive <filename>` on all affected files.

```


## File: timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py

```
#!/usr/bin/env python3
"""
TimesFM Anomaly Detection Example — Two-Phase Method

Phase 1 (context): Linear detrend + Z-score on 36 months of real NOAA
  temperature anomaly data (2022-01 through 2024-12).
  Sep 2023 (1.47 C) is a known critical outlier.

Phase 2 (forecast): TimesFM quantile prediction intervals on a 12-month
  synthetic future with 3 injected anomalies.

Outputs:
  output/anomaly_detection.png  -- 2-panel visualization
  output/anomaly_detection.json -- structured detection records
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HORIZON = 12
DATA_FILE = (
    Path(__file__).parent.parent / "global-temperature" / "temperature_anomaly.csv"
)
OUTPUT_DIR = Path(__file__).parent / "output"

CRITICAL_Z = 3.0
WARNING_Z = 2.0

# quant_fc index mapping: 0=mean, 1=q10, 2=q20, ..., 9=q90
IDX_Q10, IDX_Q20, IDX_Q80, IDX_Q90 = 1, 2, 8, 9

CLR = {"CRITICAL": "#e02020", "WARNING": "#f08030", "NORMAL": "#4a90d9"}


# ---------------------------------------------------------------------------
# Phase 1: context anomaly detection
# ---------------------------------------------------------------------------


def detect_context_anomalies(
    values: np.ndarray,
    dates: list,
) -> tuple[list[dict], np.ndarray, np.ndarray, float]:
    """Linear detrend + Z-score anomaly detection on context period.

    Returns
    -------
    records    : list of dicts, one per month
    trend_line : fitted linear trend values (same length as values)
    residuals  : actual - trend_line
    res_std    : std of residuals (used as sigma for threshold bands)
    """
    n = len(values)
    idx = np.arange(n, dtype=float)

    coeffs = np.polyfit(idx, values, 1)
    trend_line = np.polyval(coeffs, idx)
    residuals = values - trend_line
    res_std = residuals.std()

    records = []
    for i, (d, v, r) in enumerate(zip(dates, values, residuals)):
        z = r / res_std if res_std > 0 else 0.0
        if abs(z) >= CRITICAL_Z:
            severity = "CRITICAL"
        elif abs(z) >= WARNING_Z:
            severity = "WARNING"
        else:
            severity = "NORMAL"
        records.append(
            {
                "date": str(d)[:7],
                "value": round(float(v), 4),
                "trend": round(float(trend_line[i]), 4),
                "residual": round(float(r), 4),
                "z_score": round(float(z), 3),
                "severity": severity,
            }
        )
    return records, trend_line, residuals, res_std


# ---------------------------------------------------------------------------
# Phase 2: synthetic future + forecast anomaly detection
# ---------------------------------------------------------------------------


def build_synthetic_future(
    context: np.ndarray,
    n: int,
    seed: int = 42,
) -> tuple[np.ndarray, list[int]]:
    """Build a plausible future with 3 injected anomalies.

    Injected months: 3, 8, 11 (0-indexed within the 12-month horizon).
    Returns (future_values, injected_indices).
    """
    rng = np.random.default_rng(seed)
    trend = np.linspace(context[-6:].mean(), context[-6:].mean() + 0.05, n)
    noise = rng.normal(0, 0.1, n)
    future = trend + noise

    injected = [3, 8, 11]
    future[3] += 0.7  # CRITICAL spike
    future[8] -= 0.65  # CRITICAL dip
    future[11] += 0.45  # WARNING spike

    return future.astype(np.float32), injected


def detect_forecast_anomalies(
    future_values: np.ndarray,
    point: np.ndarray,
    quant_fc: np.ndarray,
    future_dates: list,
    injected_at: list[int],
) -> list[dict]:
    """Classify each forecast month by which PI band it falls outside.

    CRITICAL = outside 80% PI (q10-q90)
    WARNING  = outside 60% PI (q20-q80) but inside 80% PI
    NORMAL   = inside 60% PI
    """
    q10 = quant_fc[IDX_Q10]
    q20 = quant_fc[IDX_Q20]
    q80 = quant_fc[IDX_Q80]
    q90 = quant_fc[IDX_Q90]

    records = []
    for i, (d, fv, pt) in enumerate(zip(future_dates, future_values, point)):
        outside_80 = fv < q10[i] or fv > q90[i]
        outside_60 = fv < q20[i] or fv > q80[i]

        if outside_80:
            severity = "CRITICAL"
        elif outside_60:
            severity = "WARNING"
        else:
            severity = "NORMAL"

        records.append(
            {
                "date": str(d)[:7],
                "actual": round(float(fv), 4),
                "forecast": round(float(pt), 4),
                "q10": round(float(q10[i]), 4),
                "q20": round(float(q20[i]), 4),
                "q80": round(float(q80[i]), 4),
                "q90": round(float(q90[i]), 4),
                "severity": severity,
                "was_injected": i in injected_at,
            }
        )
    return records


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------


def plot_results(
    context_dates: list,
    context_values: np.ndarray,
    ctx_records: list[dict],
    trend_line: np.ndarray,
    residuals: np.ndarray,
    res_std: float,
    future_dates: list,
    future_values: np.ndarray,
    point_fc: np.ndarray,
    quant_fc: np.ndarray,
    fc_records: list[dict],
) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={"hspace": 0.42})
    fig.suptitle(
        "TimesFM Anomaly Detection — Two-Phase Method", fontsize=14, fontweight="bold"
    )

    # -----------------------------------------------------------------------
    # Panel 1 — full timeline
    # -----------------------------------------------------------------------
    ctx_x = [pd.Timestamp(d) for d in context_dates]
    fut_x = [pd.Timestamp(d) for d in future_dates]
    divider = ctx_x[-1]

    # context: blue line + trend + 2sigma band
    ax1.plot(
        ctx_x,
        context_values,
        color=CLR["NORMAL"],
        lw=2,
        marker="o",
        ms=4,
        label="Observed (context)",
    )
    ax1.plot(ctx_x, trend_line, color="#aaaaaa", lw=1.5, ls="--", label="Linear trend")
    ax1.fill_between(
        ctx_x,
        trend_line - 2 * res_std,
        trend_line + 2 * res_std,
        alpha=0.15,
        color=CLR["NORMAL"],
        label="+/-2sigma band",
    )

    # context anomaly markers
    seen_ctx: set[str] = set()
    for rec in ctx_records:
        if rec["severity"] == "NORMAL":
            continue
        d = pd.Timestamp(rec["date"])
        v = rec["value"]
        sev = rec["severity"]
        lbl = f"Context {sev}" if sev not in seen_ctx else None
        seen_ctx.add(sev)
        ax1.scatter(d, v, marker="D", s=90, color=CLR[sev], zorder=6, label=lbl)
        ax1.annotate(
            f"z={rec['z_score']:+.1f}",
            (d, v),
            textcoords="offset points",
            xytext=(0, 9),
            fontsize=7.5,
            ha="center",
            color=CLR[sev],
        )

    # forecast section
    q10 = quant_fc[IDX_Q10]
    q20 = quant_fc[IDX_Q20]
    q80 = quant_fc[IDX_Q80]
    q90 = quant_fc[IDX_Q90]

    ax1.plot(fut_x, future_values, "k--", lw=1.5, label="Synthetic future (truth)")
    ax1.plot(
        fut_x,
        point_fc,
        color=CLR["CRITICAL"],
        lw=2,
        marker="s",
        ms=4,
        label="TimesFM point forecast",
    )
    ax1.fill_between(fut_x, q10, q90, alpha=0.15, color=CLR["CRITICAL"], label="80% PI")
    ax1.fill_between(fut_x, q20, q80, alpha=0.25, color=CLR["CRITICAL"], label="60% PI")

    seen_fc: set[str] = set()
    for i, rec in enumerate(fc_records):
        if rec["severity"] == "NORMAL":
            continue
        d = pd.Timestamp(rec["date"])
        v = rec["actual"]
        sev = rec["severity"]
        mk = "X" if sev == "CRITICAL" else "^"
        lbl = f"Forecast {sev}" if sev not in seen_fc else None
        seen_fc.add(sev)
        ax1.scatter(d, v, marker=mk, s=100, color=CLR[sev], zorder=6, label=lbl)

    ax1.axvline(divider, color="#555555", lw=1.5, ls=":")
    ax1.text(
        divider,
        ax1.get_ylim()[1] if ax1.get_ylim()[1] != 0 else 1.5,
        "  <- Context | Forecast ->",
        fontsize=8.5,
        color="#555555",
        style="italic",
        va="top",
    )

    ax1.annotate(
        "Context: D = Z-score anomaly | Forecast: X = CRITICAL, ^ = WARNING",
        xy=(0.01, 0.04),
        xycoords="axes fraction",
        fontsize=8,
        bbox=dict(boxstyle="round", fc="white", ec="#cccccc", alpha=0.9),
    )

    ax1.set_ylabel("Temperature Anomaly (C)", fontsize=10)
    ax1.legend(ncol=2, fontsize=7.5, loc="upper left")
    ax1.grid(True, alpha=0.22)

    # -----------------------------------------------------------------------
    # Panel 2 — deviation bars across all 48 months
    # -----------------------------------------------------------------------
    all_labels: list[str] = []
    bar_colors: list[str] = []
    bar_heights: list[float] = []

    for rec in ctx_records:
        all_labels.append(rec["date"])
        bar_heights.append(rec["residual"])
        bar_colors.append(CLR[rec["severity"]])

    fc_deviations: list[float] = []
    for rec in fc_records:
        all_labels.append(rec["date"])
        dev = rec["actual"] - rec["forecast"]
        fc_deviations.append(dev)
        bar_heights.append(dev)
        bar_colors.append(CLR[rec["severity"]])

    xs = np.arange(len(all_labels))
    ax2.bar(xs[:36], bar_heights[:36], color=bar_colors[:36], alpha=0.8)
    ax2.bar(xs[36:], bar_heights[36:], color=bar_colors[36:], alpha=0.8)

    # threshold lines for context section only
    ax2.hlines(
        [2 * res_std, -2 * res_std], -0.5, 35.5, colors=CLR["NORMAL"], lw=1.2, ls="--"
    )
    ax2.hlines(
        [3 * res_std, -3 * res_std], -0.5, 35.5, colors=CLR["NORMAL"], lw=1.0, ls=":"
    )

    # PI bands for forecast section
    fc_xs = xs[36:]
    ax2.fill_between(
        fc_xs,
        q10 - point_fc,
        q90 - point_fc,
        alpha=0.12,
        color=CLR["CRITICAL"],
        step="mid",
    )
    ax2.fill_between(
        fc_xs,
        q20 - point_fc,
        q80 - point_fc,
        alpha=0.20,
        color=CLR["CRITICAL"],
        step="mid",
    )

    ax2.axvline(35.5, color="#555555", lw=1.5, ls="--")
    ax2.axhline(0, color="black", lw=0.8, alpha=0.6)

    ax2.text(
        10,
        ax2.get_ylim()[0] * 0.85 if ax2.get_ylim()[0] < 0 else -0.05,
        "<- Context: delta from linear trend",
        fontsize=8,
        style="italic",
        color="#555555",
        ha="center",
    )
    ax2.text(
        41,
        ax2.get_ylim()[0] * 0.85 if ax2.get_ylim()[0] < 0 else -0.05,
        "Forecast: delta from TimesFM ->",
        fontsize=8,
        style="italic",
        color="#555555",
        ha="center",
    )

    tick_every = 3
    ax2.set_xticks(xs[::tick_every])
    ax2.set_xticklabels(all_labels[::tick_every], rotation=45, ha="right", fontsize=7)
    ax2.set_ylabel("Delta from expected (C)", fontsize=10)
    ax2.grid(True, alpha=0.22, axis="y")

    legend_patches = [
        mpatches.Patch(color=CLR["CRITICAL"], label="CRITICAL"),
        mpatches.Patch(color=CLR["WARNING"], label="WARNING"),
        mpatches.Patch(color=CLR["NORMAL"], label="Normal"),
    ]
    ax2.legend(handles=legend_patches, fontsize=8, loc="upper right")

    output_path = OUTPUT_DIR / "anomaly_detection.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 68)
    print("  TIMESFM ANOMALY DETECTION — TWO-PHASE METHOD")
    print("=" * 68)

    # --- Load context data ---------------------------------------------------
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    context_values = df["anomaly_c"].values.astype(np.float32)
    context_dates = [pd.Timestamp(d) for d in df["date"].tolist()]
    start_str = context_dates[0].strftime('%Y-%m') if not pd.isnull(context_dates[0]) else '?'
    end_str   = context_dates[-1].strftime('%Y-%m') if not pd.isnull(context_dates[-1]) else '?'
    print(f"\n  Context: {len(context_values)} months  ({start_str} - {end_str})")

    # --- Phase 1: context anomaly detection ----------------------------------
    ctx_records, trend_line, residuals, res_std = detect_context_anomalies(
        context_values, context_dates
    )
    ctx_critical = [r for r in ctx_records if r["severity"] == "CRITICAL"]
    ctx_warning = [r for r in ctx_records if r["severity"] == "WARNING"]
    print(f"\n  [Phase 1] Context anomalies (Z-score, sigma={res_std:.3f} C):")
    print(f"    CRITICAL (|Z|>={CRITICAL_Z}): {len(ctx_critical)}")
    for r in ctx_critical:
        print(f"      {r['date']}  {r['value']:+.3f} C  z={r['z_score']:+.2f}")
    print(f"    WARNING  (|Z|>={WARNING_Z}): {len(ctx_warning)}")
    for r in ctx_warning:
        print(f"      {r['date']}  {r['value']:+.3f} C  z={r['z_score']:+.2f}")

    # --- Load TimesFM --------------------------------------------------------
    print("\n  Loading TimesFM 1.0 ...")
    import timesfm

    hparams = timesfm.TimesFmHparams(horizon_len=HORIZON)
    checkpoint = timesfm.TimesFmCheckpoint(
        huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
    )
    model = timesfm.TimesFm(hparams=hparams, checkpoint=checkpoint)

    point_out, quant_out = model.forecast([context_values], freq=[0])
    point_fc = point_out[0]  # shape (HORIZON,)
    quant_fc = quant_out[0].T  # shape (10, HORIZON)

    # --- Build synthetic future + Phase 2 detection --------------------------
    future_values, injected = build_synthetic_future(context_values, HORIZON)
    last_date = context_dates[-1]
    future_dates = [last_date + pd.DateOffset(months=i + 1) for i in range(HORIZON)]

    fc_records = detect_forecast_anomalies(
        future_values, point_fc, quant_fc, future_dates, injected
    )
    fc_critical = [r for r in fc_records if r["severity"] == "CRITICAL"]
    fc_warning = [r for r in fc_records if r["severity"] == "WARNING"]

    print(f"\n  [Phase 2] Forecast anomalies (quantile PI, horizon={HORIZON} months):")
    print(f"    CRITICAL (outside 80% PI): {len(fc_critical)}")
    for r in fc_critical:
        print(
            f"      {r['date']}  actual={r['actual']:+.3f}  "
            f"fc={r['forecast']:+.3f}  injected={r['was_injected']}"
        )
    print(f"    WARNING  (outside 60% PI): {len(fc_warning)}")
    for r in fc_warning:
        print(
            f"      {r['date']}  actual={r['actual']:+.3f}  "
            f"fc={r['forecast']:+.3f}  injected={r['was_injected']}"
        )

    # --- Plot ----------------------------------------------------------------
    print("\n  Generating 2-panel visualization...")
    plot_results(
        context_dates,
        context_values,
        ctx_records,
        trend_line,
        residuals,
        res_std,
        future_dates,
        future_values,
        point_fc,
        quant_fc,
        fc_records,
    )

    # --- Save JSON -----------------------------------------------------------
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = {
        "method": "two_phase",
        "context_method": "linear_detrend_zscore",
        "forecast_method": "quantile_prediction_intervals",
        "thresholds": {
            "critical_z": CRITICAL_Z,
            "warning_z": WARNING_Z,
            "pi_critical_pct": 80,
            "pi_warning_pct": 60,
        },
        "context_summary": {
            "total": len(ctx_records),
            "critical": len(ctx_critical),
            "warning": len(ctx_warning),
            "norm
```


## File: timesfm-forecasting/examples/anomaly-detection/output/anomaly_detection.json

```
{
  "method": "two_phase",
  "context_method": "linear_detrend_zscore",
  "forecast_method": "quantile_prediction_intervals",
  "thresholds": {
    "critical_z": 3.0,
    "warning_z": 2.0,
    "pi_critical_pct": 80,
    "pi_warning_pct": 60
  },
  "context_summary": {
    "total": 36,
    "critical": 1,
    "warning": 0,
    "normal": 35,
    "res_std": 0.11362
  },
  "forecast_summary": {
    "total": 12,
    "critical": 4,
    "warning": 1,
    "normal": 7
  },
  "context_detections": [
    {
      "date": "2022-01",
      "value": 0.89,
      "trend": 0.837,
      "residual": 0.053,
      "z_score": 0.467,
      "severity": "NORMAL"
    },
    {
      "date": "2022-02",
      "value": 0.89,
      "trend": 0.8514,
      "residual": 0.0386,
      "z_score": 0.34,
      "severity": "NORMAL"
    },
    {
      "date": "2022-03",
      "value": 1.02,
      "trend": 0.8658,
      "residual": 0.1542,
      "z_score": 1.357,
      "severity": "NORMAL"
    },
    {
      "date": "2022-04",
      "value": 0.88,
      "trend": 0.8803,
      "residual": -0.0003,
      "z_score": -0.002,
      "severity": "NORMAL"
    },
    {
      "date": "2022-05",
      "value": 0.85,
      "trend": 0.8947,
      "residual": -0.0447,
      "z_score": -0.394,
      "severity": "NORMAL"
    },
    {
      "date": "2022-06",
      "value": 0.88,
      "trend": 0.9092,
      "residual": -0.0292,
      "z_score": -0.257,
      "severity": "NORMAL"
    },
    {
      "date": "2022-07",
      "value": 0.88,
      "trend": 0.9236,
      "residual": -0.0436,
      "z_score": -0.384,
      "severity": "NORMAL"
    },
    {
      "date": "2022-08",
      "value": 0.9,
      "trend": 0.9381,
      "residual": -0.0381,
      "z_score": -0.335,
      "severity": "NORMAL"
    },
    {
      "date": "2022-09",
      "value": 0.88,
      "trend": 0.9525,
      "residual": -0.0725,
      "z_score": -0.638,
      "severity": "NORMAL"
    },
    {
      "date": "2022-10",
      "value": 0.95,
      "trend": 0.9669,
      "residual": -0.0169,
      "z_score": -0.149,
      "severity": "NORMAL"
    },
    {
      "date": "2022-11",
      "value": 0.77,
      "trend": 0.9814,
      "residual": -0.2114,
      "z_score": -1.86,
      "severity": "NORMAL"
    },
    {
      "date": "2022-12",
      "value": 0.78,
      "trend": 0.9958,
      "residual": -0.2158,
      "z_score": -1.9,
      "severity": "NORMAL"
    },
    {
      "date": "2023-01",
      "value": 0.87,
      "trend": 1.0103,
      "residual": -0.1403,
      "z_score": -1.235,
      "severity": "NORMAL"
    },
    {
      "date": "2023-02",
      "value": 0.98,
      "trend": 1.0247,
      "residual": -0.0447,
      "z_score": -0.394,
      "severity": "NORMAL"
    },
    {
      "date": "2023-03",
      "value": 1.21,
      "trend": 1.0392,
      "residual": 0.1708,
      "z_score": 1.503,
      "severity": "NORMAL"
    },
    {
      "date": "2023-04",
      "value": 1.0,
      "trend": 1.0536,
      "residual": -0.0536,
      "z_score": -0.472,
      "severity": "NORMAL"
    },
    {
      "date": "2023-05",
      "value": 0.94,
      "trend": 1.0681,
      "residual": -0.1281,
      "z_score": -1.127,
      "severity": "NORMAL"
    },
    {
      "date": "2023-06",
      "value": 1.08,
      "trend": 1.0825,
      "residual": -0.0025,
      "z_score": -0.022,
      "severity": "NORMAL"
    },
    {
      "date": "2023-07",
      "value": 1.18,
      "trend": 1.0969,
      "residual": 0.0831,
      "z_score": 0.731,
      "severity": "NORMAL"
    },
    {
      "date": "2023-08",
      "value": 1.24,
      "trend": 1.1114,
      "residual": 0.1286,
      "z_score": 1.132,
      "severity": "NORMAL"
    },
    {
      "date": "2023-09",
      "value": 1.47,
      "trend": 1.1258,
      "residual": 0.3442,
      "z_score": 3.029,
      "severity": "CRITICAL"
    },
    {
      "date": "2023-10",
      "value": 1.32,
      "trend": 1.1403,
      "residual": 0.1797,
      "z_score": 1.582,
      "severity": "NORMAL"
    },
    {
      "date": "2023-11",
      "value": 1.18,
      "trend": 1.1547,
      "residual": 0.0253,
      "z_score": 0.222,
      "severity": "NORMAL"
    },
    {
      "date": "2023-12",
      "value": 1.16,
      "trend": 1.1692,
      "residual": -0.0092,
      "z_score": -0.081,
      "severity": "NORMAL"
    },
    {
      "date": "2024-01",
      "value": 1.22,
      "trend": 1.1836,
      "residual": 0.0364,
      "z_score": 0.32,
      "severity": "NORMAL"
    },
    {
      "date": "2024-02",
      "value": 1.35,
      "trend": 1.1981,
      "residual": 0.1519,
      "z_score": 1.337,
      "severity": "NORMAL"
    },
    {
      "date": "2024-03",
      "value": 1.34,
      "trend": 1.2125,
      "residual": 0.1275,
      "z_score": 1.122,
      "severity": "NORMAL"
    },
    {
      "date": "2024-04",
      "value": 1.26,
      "trend": 1.2269,
      "residual": 0.0331,
      "z_score": 0.291,
      "severity": "NORMAL"
    },
    {
      "date": "2024-05",
      "value": 1.15,
      "trend": 1.2414,
      "residual": -0.0914,
      "z_score": -0.804,
      "severity": "NORMAL"
    },
    {
      "date": "2024-06",
      "value": 1.2,
      "trend": 1.2558,
      "residual": -0.0558,
      "z_score": -0.491,
      "severity": "NORMAL"
    },
    {
      "date": "2024-07",
      "value": 1.24,
      "trend": 1.2703,
      "residual": -0.0303,
      "z_score": -0.266,
      "severity": "NORMAL"
    },
    {
      "date": "2024-08",
      "value": 1.3,
      "trend": 1.2847,
      "residual": 0.0153,
      "z_score": 0.135,
      "severity": "NORMAL"
    },
    {
      "date": "2024-09",
      "value": 1.28,
      "trend": 1.2992,
      "residual": -0.0192,
      "z_score": -0.169,
      "severity": "NORMAL"
    },
    {
      "date": "2024-10",
      "value": 1.27,
      "trend": 1.3136,
      "residual": -0.0436,
      "z_score": -0.384,
      "severity": "NORMAL"
    },
    {
      "date": "2024-11",
      "value": 1.22,
      "trend": 1.328,
      "residual": -0.108,
      "z_score": -0.951,
      "severity": "NORMAL"
    },
    {
      "date": "2024-12",
      "value": 1.2,
      "trend": 1.3425,
      "residual": -0.1425,
      "z_score": -1.254,
      "severity": "NORMAL"
    }
  ],
  "forecast_detections": [
    {
      "date": "2025-01",
      "actual": 1.2821,
      "forecast": 1.2593,
      "q10": 1.1407,
      "q20": 1.1881,
      "q80": 1.324,
      "q90": 1.3679,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-02",
      "actual": 1.1522,
      "forecast": 1.2857,
      "q10": 1.1406,
      "q20": 1.1961,
      "q80": 1.3751,
      "q90": 1.4254,
      "severity": "WARNING",
      "was_injected": false
    },
    {
      "date": "2025-03",
      "actual": 1.3358,
      "forecast": 1.295,
      "q10": 1.1269,
      "q20": 1.1876,
      "q80": 1.4035,
      "q90": 1.4643,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-04",
      "actual": 2.0594,
      "forecast": 1.2208,
      "q10": 1.0353,
      "q20": 1.1042,
      "q80": 1.331,
      "q90": 1.4017,
      "severity": "CRITICAL",
      "was_injected": true
    },
    {
      "date": "2025-05",
      "actual": 1.0747,
      "forecast": 1.1703,
      "q10": 0.9691,
      "q20": 1.0431,
      "q80": 1.2892,
      "q90": 1.3632,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-06",
      "actual": 1.1442,
      "forecast": 1.1456,
      "q10": 0.942,
      "q20": 1.0111,
      "q80": 1.2703,
      "q90": 1.3454,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-07",
      "actual": 1.2917,
      "forecast": 1.1702,
      "q10": 0.9504,
      "q20": 1.0348,
      "q80": 1.2998,
      "q90": 1.3807,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-08",
      "actual": 1.2519,
      "forecast": 1.2027,
      "q10": 0.9709,
      "q20": 1.0594,
      "q80": 1.3408,
      "q90": 1.4195,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-09",
      "actual": 0.6364,
      "forecast": 1.191,
      "q10": 0.9594,
      "q20": 1.0404,
      "q80": 1.3355,
      "q90": 1.417,
      "severity": "CRITICAL",
      "was_injected": true
    },
    {
      "date": "2025-10",
      "actual": 1.2073,
      "forecast": 1.1491,
      "q10": 0.9079,
      "q20": 0.9953,
      "q80": 1.2869,
      "q90": 1.3775,
      "severity": "NORMAL",
      "was_injected": false
    },
    {
      "date": "2025-11",
      "actual": 1.3851,
      "forecast": 1.0805,
      "q10": 0.8361,
      "q20": 0.926,
      "q80": 1.2284,
      "q90": 1.3122,
      "severity": "CRITICAL",
      "was_injected": false
    },
    {
      "date": "2025-12",
      "actual": 1.8294,
      "forecast": 1.0613,
      "q10": 0.8022,
      "q20": 0.8952,
      "q80": 1.2169,
      "q90": 1.296,
      "severity": "CRITICAL",
      "was_injected": true
    }
  ]
}
```


(… 69 more files omitted due to size limit)
<!-- fetched-content:end -->
