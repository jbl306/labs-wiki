---
title: "https://github.com/google-research/timesfm"
type: url
captured: 2026-04-13T17:25:04.763317+00:00
source: android-share
url: "https://github.com/google-research/timesfm"
content_hash: "sha256:52a49b8215a214a6c2a2b89a30061410e06dd292516a3860bb1435db8620fe60"
tags: []
status: ingested
---

https://github.com/google-research/timesfm

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T06:05:06+00:00
- source_url: https://github.com/google-research/timesfm
- resolved_url: https://github.com/google-research/timesfm
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: google-research/timesfm
Description: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.
Stars: 18254
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


## File: v1/docs/contributing.md

```
# How to Contribute

We would love to accept your patches and contributions to this project.

## Before you begin

### Sign our Contributor License Agreement

Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
You (or your employer) retain the copyright to your contribution; this simply
gives us permission to use and redistribute your contributions as part of the
project.

If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.

Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.

### Review our Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Contribution process

### Code Reviews

All submissions, including submissions by project members, require review. We
use [GitHub pull requests](https://docs.github.com/articles/about-pull-requests)
for this purpose.

```


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


## File: AGENTS.md

```
# TimesFM — Agent Entry Point

This repository ships a first-party **Agent Skill** for TimesFM at:

```
timesfm-forecasting/
└── SKILL.md    ← read this for the full skill
```

## Install the skill

Copy the skill directory into your agent's skills folder:

```bash
# Cursor / Claude Code / OpenCode / Codex (global install)
cp -r timesfm-forecasting/ ~/.cursor/skills/
cp -r timesfm-forecasting/ ~/.claude/skills/

# Or project-level
cp -r timesfm-forecasting/ .cursor/skills/
```

Any agent that supports the open [Agent Skills standard](https://agentskills.io) will discover it automatically.

## Working in this repo

If you are developing TimesFM itself (not using it), the source lives in `src/timesfm/`.
Archived v1/v2 code and notebooks are in `v1/`.

Run tests:

```bash
pytest v1/tests/
```

See `README.md` for full developer setup.

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
      origin of the Work and reproducing t
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


## File: .github/workflows/main.yml

```
name: Python package build

on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      - name: Create virtual environment
        run: uv venv
      - name: Install build dependencies
        run: |
          uv pip install build ".[torch,flax]"
      - name: Build package
        run: uv run python -m build
```


## File: .github/workflows/manual_publish.yml

```
name: Manual PyPI Publish

on:
  workflow_dispatch:

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      - name: Create virtual environment
        run: uv venv
      - name: Install build dependencies
        run: uv pip install build twine
      - name: Build package
        run: uv run python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: uv run twine upload dist/*
```


## File: src/timesfm/__init__.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TimesFM API."""

from .configs import ForecastConfig

try:
  from .timesfm_2p5 import timesfm_2p5_torch
  TimesFM_2p5_200M_torch = timesfm_2p5_torch.TimesFM_2p5_200M_torch
except ImportError:
  pass

try:
  from .timesfm_2p5 import timesfm_2p5_flax
  TimesFM_2p5_200M_flax = timesfm_2p5_flax.TimesFM_2p5_200M_flax
except ImportError:
  pass

```


## File: src/timesfm/configs.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstract configs for TimesFM layers."""

import dataclasses
from typing import Literal


@dataclasses.dataclass(frozen=True)
class ForecastConfig:
  """Options for forecasting.

  Attributes:
    max_context: The maximum context length. This is used by the compiled decode
      function at inference time during batched inference. Any input time series
      with length less than max_context will be padded with zeros, and with
      length greater than max_context will be truncated.
    max_horizon: The maximum horizon length. This is used by the compiled decode
      function at inference time during batched inference. The compiled cached
      decoding function will by default forecast till max_horizon.
    normalize_inputs: Whether to normalize the inputs. This is useful when the
      raw inputs are of extremely large or small magnitudes which may result in
      numerical issues.
    window_size: The window size for decomposed forecasting.
      TODO(siriuz42):implement it.
    per_core_batch_size: The batch size per core. Used at inference time during
      batched inference when multiple GPU / TPU devices are used.
    use_continuous_quantile_head: Whether to use a separate continuous quantile
      head to avoid quantile collapsing.
    force_flip_invariance: Whether to force flip invariance. TimesFM guarantees
      that TimesFM(aX + b) = a * TimesFM(x) + b for a >= 0 by default. This flag
      extends it to a < 0 as well.
    infer_is_positive: Whether to guarantee nonnegativity of the output if the
      input is nonnegative.
    fix_quantile_crossing: Whether to fix quantile crossing.
    return_backcast: Whether to return backcast.
  """

  max_context: int = 0
  max_horizon: int = 0
  normalize_inputs: bool = False
  window_size: int = 0
  per_core_batch_size: int = 1
  use_continuous_quantile_head: bool = False
  force_flip_invariance: bool = True
  infer_is_positive: bool = True
  fix_quantile_crossing: bool = False
  return_backcast: bool = False


@dataclasses.dataclass(frozen=True)
class ResidualBlockConfig:
  """Framework-agnostic config for a residual block."""

  input_dims: int
  hidden_dims: int
  output_dims: int
  use_bias: bool
  activation: Literal["relu", "swish", "none"]


@dataclasses.dataclass(frozen=True)
class RandomFourierFeaturesConfig:
  """Framework-agnostic config for random fourier features."""

  input_dims: int
  output_dims: int
  projection_stddev: float
  use_bias: bool


@dataclasses.dataclass(frozen=True)
class TransformerConfig:
  """Framework-agnostic config for a transformer."""

  model_dims: int
  hidden_dims: int
  num_heads: int
  attention_norm: Literal["rms"]
  feedforward_norm: Literal["rms"]
  qk_norm: Literal["rms", "none"]
  use_bias: bool
  use_rotary_position_embeddings: bool
  ff_activation: Literal["relu", "swish", "none"]
  fuse_qkv: bool


@dataclasses.dataclass(frozen=True)
class StackedTransformersConfig:
  """Framework-agnostic config for a stacked transformers."""

  num_layers: int
  transformer: TransformerConfig

```


## File: src/timesfm/flax/__init__.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

```


## File: src/timesfm/flax/dense.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dense layers for TimesFM."""

from flax import nnx
import jax
import jax.numpy as jnp
import jaxtyping

from .. import configs

Array = jaxtyping.Array
Bool = jaxtyping.Bool
Float = jaxtyping.Float
Integer = jaxtyping.Integer
Num = jaxtyping.Num

ResidualBlockConfig = configs.ResidualBlockConfig
RandomFourierFeaturesConfig = configs.RandomFourierFeaturesConfig


class ResidualBlock(nnx.Module):
  """Residual block with two linear layers and a linear residual connection."""

  def __init__(self, config: ResidualBlockConfig, *, rngs=nnx.Rngs(42)):
    self.config = config
    self.hidden_layer = nnx.Linear(
      in_features=config.input_dims,
      out_features=config.hidden_dims,
      use_bias=config.use_bias,
      rngs=rngs,
    )
    self.output_layer = nnx.Linear(
      in_features=config.hidden_dims,
      out_features=config.output_dims,
      use_bias=config.use_bias,
      rngs=rngs,
    )
    self.residual_layer = nnx.Linear(
      in_features=config.input_dims,
      out_features=config.output_dims,
      use_bias=config.use_bias,
      rngs=rngs,
    )
    if config.activation == "relu":
      self.activation = jax.nn.relu
    elif config.activation == "swish":
      self.activation = jax.nn.swish
    elif config.activation == "none":
      self.activation = lambda x: x
    else:
      raise ValueError(f"Activation: {config.activation} not supported.")

  def __call__(self, x: Float[Array, "b ... i"]) -> Float[Array, "b ... o"]:
    return self.output_layer(
      self.activation(self.hidden_layer(x))
    ) + self.residual_layer(x)


class RandomFourierFeatures(nnx.Module):
  """Random Fourier features layer."""

  __data__ = ("phrase_shifts",)

  def __init__(self, config: RandomFourierFeaturesConfig, *, rngs=nnx.Rngs(42)):
    self.config = config

    if config.output_dims % 4 != 0:
      raise ValueError(
        f"Output dims must be a multiple of 4: {config.output_dims} % 4 != 0."
      )
    num_projected_features = config.output_dims // 4

    self.phase_shifts = nnx.Param(jnp.zeros(shape=(2, num_projected_features)))
    self.projection_layer = nnx.Linear(
      in_features=config.input_dims,
      out_features=num_projected_features,
      use_bias=config.use_bias,
      rngs=rngs,
    )
    self.residual_layer = nnx.Linear(
      in_features=config.input_dims,
      out_features=config.output_dims,
      use_bias=config.use_bias,
      rngs=rngs,
    )

  def __call__(self, x: Float[Array, "b ... i"]) -> Float[Array, "b ... o"]:
    projected = self.projection_layer(x)
    cos_features = jnp.cos(projected)
    sin_features = jnp.sin(projected)
    sq_wave_1 = jnp.sign(jnp.sin(projected + self.phase_shifts[0, :]))
    sq_wave_2 = jnp.sign(jnp.sin(projected + self.phase_shifts[1, :]))
    fourier_features = jnp.concatenate(
      [cos_features, sin_features, sq_wave_1, sq_wave_2], axis=-1
    )
    residual = self.residual_layer(x)
    return fourier_features + residual

```


## File: src/timesfm/flax/normalization.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Normalization layers for TimesFM."""

from flax import nnx
import jax
import jax.numpy as jnp
import jaxtyping

Array = jaxtyping.Array
Bool = jaxtyping.Bool
Float = jaxtyping.Float
Integer = jaxtyping.Integer
Num = jaxtyping.Num


class RMSNorm(nnx.Module):
  """RMS normalization."""

  __data__ = ("scale",)

  def __init__(
    self,
    num_features: int,
    *,
    epsilon: float = 1e-6,
    rngs=nnx.Rngs(42),
  ):
    del rngs
    self.scale = nnx.Param(jnp.zeros(shape=(num_features,)))
    self.num_features = num_features
    self.epsilon = epsilon

  def __call__(self, inputs: Float[Array, "b ... d"]) -> Float[Array, "b ... d"]:
    var = jnp.mean(jnp.square(inputs), axis=-1, keepdims=True)
    normed_inputs = inputs * jax.lax.rsqrt(var + self.epsilon)
    normed_inputs *= self.scale
    return normed_inputs


class LayerNorm(nnx.Module):
  """Layer normalization replica of  LayerNorm."""

  __data__ = ("scale", "bias")

  def __init__(self, num_features: int, *, epsilon: float = 1e-6, rngs=nnx.Rngs(42)):
    del rngs
    self.scale = nnx.Param(jnp.ones(shape=(num_features,)))
    self.bias = nnx.Param(jnp.zeros(shape=(num_features,)))
    self.num_features = num_features
    self.epsilon = epsilon

  def __call__(self, inputs: Float[Array, "b ... d"]) -> Float[Array, "b ... d"]:
    mean = jnp.mean(inputs, axis=-1, keepdims=True)
    var = jnp.mean(jnp.square(inputs - mean), axis=-1, keepdims=True)
    normed_inputs = (inputs - mean) * jax.lax.rsqrt(var + self.epsilon)
    normed_inputs *= self.scale
    normed_inputs += self.bias
    return normed_inputs

```


## File: src/timesfm/flax/transformer.py

```
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transformer layers for TimesFM."""

import functools
from typing import Callable

from flax import nnx
from flax.nnx.nn import linear
import jax
from jax import lax
import jax.numpy as jnp
import jaxtyping

from .. import configs
from . import normalization, util

Array = jaxtyping.Array
Bool = jaxtyping.Bool
Float = jaxtyping.Float
Integer = jaxtyping.Integer
Num = jaxtyping.Num
LayerNorm = normalization.LayerNorm
RMSNorm = normalization.RMSNorm
LinearGeneral = linear.LinearGeneral
TransformerConfig = configs.TransformerConfig
DecodeCache = util.DecodeCache


@functools.partial(
  jax.jit,
  static_argnames=("query_length", "kv_length"),
)
def make_attn_mask(
  query_length: int,
  num_all_masked_kv: Integer[Array, "b"],
  query_index_offset: Integer[Array, "b"] | None = None,
  kv_length: int = 0,
) -> Bool[Array, "b 1 q n"]:
  """Makes attention mask."""

  if kv_length == 0:
    kv_length = query_length

  q_index = jnp.arange(query_length)[None, None, :, None]
  if query_index_offset is not None:
    q_index += query_index_offset[:, None, None, None]
  kv_index = jnp.arange(kv_length)[None, None, None, :]
  return jnp.logical_and(
    q_index >= kv_index,
    kv_index >= num_all_masked_kv[:, None, None, None],
  )


class RotaryPositionalEmbedding(nnx.Module):
  """Rotary positional embedding."""

  def __init__(
    self,
    embedding_dims: int,
    min_timescale: int = 1,
    max_timescale: int = 10000,
  ):
    self.embedding_dims = embedding_dims
    self.min_timescale = min_timescale
    self.max_timescale = max_timescale

  def __call__(
    self,
    inputs: Float[Array, "b ... d"],
    position: Array | None = None,
  ):
    """Generates a JTensor of sinusoids with different frequencies."""
    if self.embedding_dims != inputs.shape[-1]:
      raise ValueError(
        "The embedding dims of the rotary position embedding"
        "must match the hidden dimension of the inputs."
      )
    half_embedding_dim = self.embedding_dims // 2
    fraction = 2 * jnp.arange(0, half_embedding_dim) / self.embedding_dims
    timescale = (
      self.min_timescale * (self.max_timescale / self.min_timescale) ** fraction
    )
    if position is None:
      seq_length = inputs.shape[1]
      position = jnp.arange(seq_length, dtype=jnp.float32)[None, :]
    if len(inputs.shape) == 4:
      position = position[..., None, None]
      timescale = timescale[None, None, None, :]
    elif len(inputs.shape) == 3:
      position = position[..., None]
      timescale = timescale[None, None, :]
    else:
      raise ValueError("Inputs must be of rank 3 or 4.")
    sinusoid_inp = position / timescale
    sin = jnp.sin(sinusoid_inp)
    cos = jnp.cos(sinusoid_inp)
    first_half, second_half = jnp.split(inputs, 2, axis=-1)
    first_part = first_half * cos - second_half * sin
    second_part = second_half * cos + first_half * sin
    first_part = first_part.astype(None)
    second_part = second_part.astype(None)
    return jnp.concatenate([first_part, second_part], axis=-1)


class PerDimScale(nnx.Module):
  """Per-dimension scaling."""

  __data__ = ("per_dim_scale",)

  def __init__(self, num_dims: int, *, rngs=nnx.Rngs(42)):
    del rngs
    self.num_dims = num_dims
    self.per_dim_scale = nnx.Param(jnp.zeros(shape=(num_dims,)))

  def __call__(self, x: Float[Array, "b ... d"]) -> Float[Array, "b ... d"]:
    return x * (
      1.442695041 / jnp.sqrt(self.num_dims) * jax.nn.softplus(self.per_dim_scale)
    )


class MultiHeadAttention(nnx.Module):
  """Multi-head attention."""

  def __init__(
    self,
    num_heads: int,
    in_features: int,
    *,
    use_per_dim_scale: bool = True,
    use_rotary_position_embeddings: bool = True,
    use_bias: bool = False,
    deterministic: bool | None = None,
    attention_fn: Callable[..., Array] = nnx.dot_product_attention,
    qk_norm: str = "rms",
    rngs=nnx.Rngs(42),
  ):
    self.num_heads = num_heads
    self.in_features = in_features
    self.qkv_features = in_features
    self.out_features = in_features
    self.in_kv_features = in_features
    self.deterministic = deterministic
    self.use_bias = use_bias
    self.attention_fn = attention_fn
    self.qk_norm = qk_norm

    if self.qkv_features % self.num_heads != 0:
      raise ValueError(
        f"Memory dimension ({self.qkv_features}) must be divisible by "
        f"'num_heads' heads ({self.num_heads})."
      )
    self.head_dim = self.qkv_features // self.num_heads

    linear_general = functools.partial(
      LinearGeneral,
      out_features=(self.num_heads, self.head_dim),
      use_bias=self.use_bias,
    )
    # project inputs_q to multi-headed q/k/v
    # dimensions are then [batch..., length, n_heads, n_features_per_head]
    self.query = linear_general(self.in_features, rngs=rngs)
    self.key = linear_general(self.in_kv_features, rngs=rngs)
    self.value = linear_general(self.in_kv_features, rngs=rngs)

    if self.qk_norm == "rms":
      self.query_ln = RMSNorm(self.head_dim)
      self.key_ln = RMSNorm(self.head_dim)
    else:
      self.query_ln = None
      self.key_ln = None

    self.out = LinearGeneral(
      in_features=(self.num_heads, self.head_dim),
      out_features=self.out_features,
      axis=(-2, -1),
      use_bias=self.use_bias,
      rngs=rngs,
    )

    self.use_per_dim_scale = use_per_dim_scale
    self.use_rotary_position_embeddings = use_rotary_position_embeddings
    if self.use_rotary_position_embeddings:
      self.rotary_position_embedding = RotaryPositionalEmbedding(
        embedding_dims=self.head_dim,
      )
    else:
      self.rotary_position_embedding = None

    if use_per_dim_scale:
      self.per_dim_scale = PerDimScale(num_dims=self.head_dim, rngs=rngs)
    else:
      self.per_dim_scale = None

  def __call__(
    self,
    inputs_q: Array,
    *,
    decode_cache: DecodeCache | None = None,
    patch_mask: Array | None = None,
    deterministic: bool | None = None,
    sow_weights: bool = False,
  ) -> tuple[Float[Array, "b ... o"], DecodeCache | None]:
    """Applies multi-head dot product attention on the input data."""
    _, n_patches, input_in_features = inputs_q.shape
    if input_in_features != self.in_features:
      raise ValueError(
        f"Incompatible input dimension, got {input_in_features} "
        f"but module expects {self.in_features}."
      )
    if patch_mask is None:
      patch_mask = jnp.zeros_like(inputs_q.shape[:-1], dtype=jnp.bool)

    # For query: rope -> ln -> per_dim_scale
    query = self.query(inputs_q)
    key = self.key(inputs_q)
    value = self.value(inputs_q)

    if decode_cache is None:
      num_masked = jnp.sum(patch_mask.astype(jnp.int32), axis=-1, keepdims=False)
      next_index = jnp.zeros_like(num_masked, dtype=jnp.int32)
    else:
      num_masked = (
        jnp.sum(patch_mask.astype(jnp.int32), axis=-1, keepdims=False)
        + decode_cache.num_masked
      )
      next_index = decode_cache.next_index

    if self.use_rotary_position_embeddings:
      position = (
        jnp.arange(n_patches, dtype=jnp.int32)[None, :]
        + next_index[:, None]
        - num_masked[:, None]
      )
      query = self.rotary_position_embedding(query, position)
      key = self.rotary_position_embedding(key, position)
    if self.query_ln is not None:
      query = self.query_ln(query)
    if self.key_ln is not None:
      key = self.key_ln(key)
    if self.use_per_dim_scale:
      query = se
```


(… 69 more files omitted due to size limit)
<!-- fetched-content:end -->
