# Kaggle T4x2 Qualification for Higgs TTS 3 4B

[![Repository Audit](https://github.com/dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B/actions/workflows/repository-audit.yml)
![License: MIT (repository code)](https://img.shields.io/badge/code%20license-MIT-blue.svg)
![Model license: Boson Research & Non-Commercial](https://img.shields.io/badge/model%20license-Boson%20Research%20%26%20Non--Commercial-important.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyTorch FP16](https://img.shields.io/badge/PyTorch-FP16-orange.svg)
![SGLang-Omni](https://img.shields.io/badge/SGLang--Omni-0.1.7-blueviolet.svg)
![NVIDIA Tesla T4 x2](https://img.shields.io/badge/GPU-Tesla%20T4%20x2-76B900.svg)
![Kaggle](https://img.shields.io/badge/platform-Kaggle-20BEFF.svg)
![Original weights](https://img.shields.io/badge/weights-original%20%7C%20no%20quantization-success.svg)
![Human listening](https://img.shields.io/badge/core%20TTS-human%20accepted-success.svg)
![Release state](https://img.shields.io/badge/release-v1.0.0-success.svg)

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

An **independent engineering qualification and reproducibility project** for running `bosonai/higgs-tts-3-4b` with original weights on Kaggle NVIDIA Tesla T4 x2 GPUs. This repository is **not an official Boson AI release, product, service, or endorsement**.

**Built with Higgs TTS 3 licensed from Boson AI USA, Inc.** The model weights are governed by the **Boson Higgs TTS 3 Research and Non-Commercial License**, not by this repository's MIT license.

This project is deliberately evidence-first. It keeps successful runs, failed runs, human-listening decisions, benchmark authority, runtime configuration, and reproducibility tooling together so that reviewers can reproduce the same deployment path instead of relying on screenshots or unsupported performance claims.

## Release authority

| Item | Authority |
| --- | --- |
| Repository release | `v1.0.0` |
| Repository release state | **v1.0.0** |
| Release type | Annotated Git tag + GitHub Release |
| Target hardware | Kaggle NVIDIA Tesla T4 x2 |
| Model source | `dangkhoa2016/bosonai-higgs-tts-3-4b` |
| Model variation | `transformers/default` |
| Model version | `1` |
| Weight policy | Original weights, FP16 runtime, no GGUF, no release quantization |
| Core TTS acceptance | Human-accepted English, Vietnamese, and EN-VI code-switching variants retained |
| Voice-clone production claim | `PENDING_HUMAN_ACCEPTANCE` |
| Repository CI | `Repository Audit` must pass on the release commit |

- **Repository release state:** v1.0.0

Release `v1.0.0` is the first clean-history public release after repository-audit CI qualification and release-asset verification.

## What this repository proves

The project makes a deliberately narrow claim: a carefully qualified Higgs TTS 3 4B deployment can run reproducibly on Kaggle T4x2 using the retained runtime, stage placement, model mirror, scripts, notebook, and evidence in this repository.

It does **not** claim that every T4 configuration is production-safe, that every request is byte-identical across runs, that the exact neural mechanism behind onset instability is proven, or that voice cloning is perceptually production-ready.

The repository also preserves negative evidence. Single-T4 inference was functionally successful, but it failed the production-headroom requirement after warm/reference use. The accepted deployment baseline is therefore T4x2, not single-T4.

## Current acceptance matrix

| Area | Status | Evidence / interpretation |
| --- | --- | --- |
| Original-weight model load | **PASS** | Kaggle mirror Version 1, no GGUF/quantized release path |
| T4x2 server startup | **PASS** | Accepted stage placement and production scripts |
| Health/readiness contract | **PASS** | `/health` plus stage assertions and GPU checks |
| English zero-shot TTS | **ACCEPTED** | Retained human-reviewed variants |
| Vietnamese zero-shot TTS | **ACCEPTED** | Retained human-reviewed variants |
| EN-VI code switching | **ACCEPTED** | Retained human-reviewed variants |
| Official warm benchmark | **ACCEPTED** | 33/33 HTTP 200 |
| Official project-owner Kaggle run (`356925390`) | **HUMAN REVIEWED / ACCEPTED** | Machine acceptance PASS; human listening review of the fresh official Output PASS. MIX04 raw benchmark WAVs are accepted with known low raw loudness |
| Latest human-reviewed showcase (non-official Kaggle account) | **HUMAN REVIEWED** | 8/8 transport + activity PASS and human listening approved for that run |
| Single-T4 production headroom | **FAIL** | Memory exhaustion / MIX02 CUDA OOM retained as negative evidence |
| Current SLT-conditioned reference as default | **REJECTED** | Diagnostic onset improvement, undesirable Vietnamese regional/tone characteristics |
| Voice-clone production claim | **PENDING_HUMAN_ACCEPTANCE** | Runtime transport works with synthetic references; perceptual production acceptance remains open |

Machine-readable consolidated status is retained in [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json).

## Accepted T4x2 architecture

```text
                         ┌──────────────────────────────┐
                         │           CPU host           │
                         │ preprocessing / HTTP control │
                         └──────────────┬───────────────┘
                                        │
                           ┌────────────┴────────────┐
                           │                         │
                 ┌─────────▼─────────┐     ┌────────▼─────────┐
                 │      GPU 0        │     │      GPU 1       │
                 │    tts_engine     │     │  audio_encoder   │
                 │      FP16         │     │    + vocoder     │
                 └───────────────────┘     └──────────────────┘

Tensor parallelism: disabled
```

The qualified engine contract is:

| Setting | Qualified value |
| --- | --- |
| `tts_engine.gpu` | `0` |
| `audio_encoder.gpu` | `1` |
| `vocoder.gpu` | `1` |
| dtype | `float16` |
| CUDA graph | disabled |
| `max_running_requests` | `1` |
| `mem_fraction_static` | `0.72` |
| sampling backend | `pytorch` |
| attention backend | `triton` |
| tensor parallelism | disabled |

A critical fresh-environment requirement observed during qualification is:

```bash
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

This allows the observed FlashInfer cold-JIT linker path to resolve `-lcuda`.

## Qualified software environment

The retained authority was qualified with:

| Component | Qualified value |
| --- | --- |
| Python | `3.12.3` |
| PyTorch | `2.13.0+cu130` |
| SGLang | `0.5.20` |
| SGLang-Omni | `0.1.7` |
| FlashInfer | `0.6.18` |
| GPU | NVIDIA Tesla T4 x2 |
| Runtime lock | [`production/requirements-runtime-lock.txt`](production/requirements-runtime-lock.txt) |

Kaggle base images evolve. The release therefore treats the lock file, stage placement, readiness checks, and evidence as the reproducibility contract instead of assuming future notebook images will remain unchanged.

## Model authority and mount contract

Normal Kaggle execution attaches the existing Kaggle model mirror instead of downloading weights from Hugging Face:

```text
Kaggle model: dangkhoa2016/bosonai-higgs-tts-3-4b
Variation:    transformers/default
Version:      1
Mounted path: /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

The model-critical SHA256 authority is retained in [`manifests/model-critical.sha256`](manifests/model-critical.sha256), with model metadata in [`manifests/model-authority.json`](manifests/model-authority.json).

Model weights are intentionally not committed to Git and are not duplicated in GitHub Release assets.

## Fastest review path: Kaggle UI

The recommended community-review path is the production-showcase notebook:

[`notebooks/kaggle-production-showcase.ipynb`](notebooks/kaggle-production-showcase.ipynb)

### Before Run All

1. In Kaggle, import the notebook from this GitHub repository.
2. Select **GPU T4 x2**.
3. Enable **Internet** so the notebook can resolve the annotated Git tag.
4. Use **Add Input → Models** and attach:
   - `dangkhoa2016/bosonai-higgs-tts-3-4b`
   - variation `transformers/default`
   - Version `1`
5. Run all cells from a fresh session.

The notebook is intentionally release-oriented rather than a cosmetic demo. It verifies the annotated `v1.0.0` tag, checks two T4 GPUs, confirms the model mount, creates the Python 3.12 environment, starts the real service, waits for health, runs smoke validation, generates playable acceptance WAVs, reruns the benchmark, and writes `FINAL-ACCEPTANCE.json`.

See [`notebooks/README.md`](notebooks/README.md) for the exact UI workflow and reviewer checklist.

## Manual quick start on Kaggle

If you prefer the shell-based path, clone the release and attach the same model Version 1.

Create the qualified Python 3.12 environment with `uv` and install the runtime lock:

```bash
cd /kaggle/working/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B
uv venv --python /usr/bin/python3.12 --seed .venv312
.venv312/bin/python -m pip install --prefer-binary -r production/requirements-runtime-lock.txt
```

Launch the service:

```bash
export ROOT="$PWD"
export HIGGS_VENV="$PWD/.venv312"
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/start-background.sh
```

Verify readiness:

```bash
export ROOT="$PWD"
bash production/readiness.sh
```

Run the smoke request:

```bash
HIGGS_SMOKE_OUTPUT=outputs/production-smoke.wav \
  .venv312/bin/python production/smoke-request.py
```

Run the official benchmark harness into a fresh output directory:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

The wrapper protects the retained official benchmark authority from accidental overwrite.

## Validation stages

The public repository preserves a staged qualification path instead of presenting only the final successful configuration.

| Stage | Purpose | Result |
| --- | --- | --- |
| Runtime/model qualification | Confirm original-weight load and inference compatibility | PASS |
| Single-T4 functional validation | Establish whether one T4 can produce speech | Functional PASS |
| Single-T4 production-headroom qualification | Test memory headroom after warm/reference use | FAIL |
| T4x2 stage-placement qualification | Move auxiliary stages to GPU1 | PASS |
| Root-cause and perceptual audit | Localize onset failures and human-review variants | Qualified with limitations |
| Warm benchmark | Measure accepted T4x2 runtime sequentially | PASS, 33/33 |
| Public packaging | Scripts, tests, notebook, bilingual docs, CI, release assets | PASS |

## Official warm benchmark — 2026-10-09

Protocol: 11 cases × 3 repetitions, sequential requests, warm runtime. FlashInfer cold-JIT is excluded from model-generation timing.

| Metric | Result |
| --- | ---: |
| HTTP success | **33 / 33** |
| Mean latency | **6.013801 s** |
| Median latency | **5.979205 s** |
| p95 latency | **7.094262 s** |
| Mean RTF | **1.087838** |
| Aggregate RTF | **1.086832** |
| Aggregate audio | **182.6 s** |
| Aggregate wall | **198.455444 s** |
| GPU0 peak used | **10,951 MiB** |
| GPU1 peak used | **4,511 MiB** |

Benchmark methodology is documented in [`docs/benchmark-methodology.md`](docs/benchmark-methodology.md), with results in [`docs/benchmark-results.md`](docs/benchmark-results.md) and machine-readable authority in [`evidence/t4x2-official-benchmark-2026-10-09.json`](evidence/t4x2-official-benchmark-2026-10-09.json).

## Reproducibility and determinism note

Ten of eleven benchmark cases were byte-identical across the first three repetitions. EN02 diverged on the first observation, then repetitions 2-5 were byte-identical.

The retained classification is:

```text
FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE
cause: unproven
```

This repository therefore does **not** claim universal request-level bitwise determinism. It reports the observed reproducibility pattern and preserves the extra EN02 evidence instead of smoothing it into a stronger claim.

## Why T4x2 instead of one T4

Single-T4 inference was functionally successful. That alone was not enough for a production baseline.

During the retained single-T4 headroom qualification path, warm/reference use left GPU0 at approximately 14,847 MiB used with roughly 65 MiB free. A later MIX02 request hit CUDA OOM while the server itself remained healthy. The failure is retained in [`evidence/single-t4-production-headroom.json`](evidence/single-t4-production-headroom.json).

The T4x2 layout moved `audio_encoder` and `vocoder` to GPU1 while keeping `tts_engine` on GPU0. T4x2 stage-placement qualification then completed the five-case mixed-language suite with **5/5 HTTP 200**, including the previously OOM MIX02 case.

This is why the repository claims a qualified **T4x2** baseline and explicitly does not promote the single-T4 path as production-safe.

## Onset root-cause audit

Historical zero-shot samples included:

- VI02 initial-word loss;
- MIX02 initial-word loss;
- MIX03 near-silence;
- MIX04 onset/pause behavior.

The investigation ruled out tokenizer text loss, delay-pattern off-by-one behavior, codec/HTTP WAV clipping, max-token truncation, and request concurrency as the retained explanation.

The public classification is:

```text
zero-shot AR acoustic-generation/bootstrap instability before codec decode
confidence: high for layer localization; exact learned-model internal mechanism remains unproven
```

Raw-code re-decode and API WAV output correlated at approximately `0.9999998` or higher in the retained audit, supporting localization before codec decode rather than post-codec/WAV clipping.

See [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json).

## Human-listening decisions

Fixed-seed variants produced accepted VI02, MIX02, and MIX03 outputs. MIX04 was human-approved with:

```text
seed=12346
temperature=0.65
top_k=50
max_new_tokens=384
loudnorm=I=-16:TP=-1.5:LRA=7
```

The final MIX04 authority records duration `5.84 s` and SHA256 `5b97e250421eb1869c66570609be3e3094a95bf7c4c774b37aec9a40c8a7e8f9`.

Reference-conditioned SLT output improved onset behavior diagnostically, but human review found undesirable Vietnamese regional/tone characteristics. It is therefore **diagnostic only** and is not the production default.

Voice-clone runtime transport works with synthetic references, but final perceptual production acceptance remains pending. This qualification project does not use real-person voice cloning.

## Evidence authority and transparency

The evidence hierarchy is intentionally explicit:

1. **Machine-readable retained evidence** under [`evidence/`](evidence/).
2. **Benchmark authority** under [`benchmarks/t4x2-official-2026-10-09/`](benchmarks/t4x2-official-2026-10-09/).
3. **Model provenance** under [`manifests/`](manifests/).
4. **Executable reproduction path** under [`production/`](production/) and [`scripts/`](scripts/).
5. **Kaggle community-review notebook** under [`notebooks/`](notebooks/).
6. **Bilingual interpretation and boundaries** under [`docs/`](docs/).

Recommended starting points:

- [`docs/evidence-index.md`](docs/evidence-index.md)
- [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json)
- [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json)
- [`evidence/root-cause-human-review-2026-10-09.json`](evidence/root-cause-human-review-2026-10-09.json)
- [`benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json`](benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json)

Heavy benchmark WAVs, the 15,339-logical-line raw telemetry source, model weights, `.venv312`, transient caches, and captured FlashInfer cache archives are intentionally excluded from Git.

## Repository layout

```text
.
├── .github/                  # CI, governance, Dependabot, issue/PR templates
├── benchmarks/               # compact retained benchmark authority
├── docs/                     # bilingual architecture, setup, evidence, limits, history
├── evidence/                 # machine-readable qualification and acceptance records
├── manifests/                # model provenance and critical SHA256 authority
├── notebooks/                # Kaggle production-showcase / acceptance notebook
├── production/               # runtime env, launch, readiness, smoke, benchmark wrappers
├── scripts/                  # repository verifier and benchmark harness
├── tests/                    # repository/runtime/benchmark/evidence contracts
├── CHANGELOG.md              # English release history
├── CHANGELOG.vi.md           # Vietnamese release history
├── CITATION.cff              # citation metadata
├── LICENSE                   # MIT for repository-authored material
├── README.md                 # English release overview
└── README.vi.md              # Vietnamese release overview
```

## Repository audit and CI

Run the same final repository contract locally:

```bash
make verify-final
```

The GitHub Actions workflow verifies the repository on Python 3.12 and does not run heavyweight model inference in CI. The workflow uses current major GitHub Actions dependencies (`actions/checkout@v7` and `actions/setup-python@v7`) and Dependabot is configured to surface future dependency drift.

The audit checks repository structure, JSON validity, shell syntax, bilingual documentation contracts, release metadata, notebook invariants, evidence invariants, runtime contracts, benchmark schema, and forbidden large/model payloads.

## Security and privacy boundaries

- No model weights are committed to this repository.
- No Kaggle, GitHub, or Hugging Face credentials belong in tracked files.
- Release assets intentionally exclude secrets, virtual environments, bulk WAV collections, and model payloads.
- Voice-clone qualification uses synthetic references; no real-person voice cloning is required for the accepted core TTS evidence.
- Security reporting guidance is documented in [`SECURITY.md`](.github/SECURITY.md).

## Known limitations

The most important boundaries are:

- single-T4 production headroom is not accepted;
- exact onset neural mechanism remains unproven;
- universal byte-level determinism is not claimed;
- voice-clone production acceptance remains pending;
- the SLT-conditioned diagnostic reference is rejected as the default production reference;
- performance numbers apply to the retained Kaggle T4x2 qualification path, not arbitrary GPU/runtime combinations.

See [`docs/known-limitations.md`](docs/known-limitations.md) for the full list.

## Troubleshooting

Start with [`docs/troubleshooting.md`](docs/troubleshooting.md). Common high-value checks are:

1. Confirm Kaggle exposes two Tesla T4 GPUs.
2. Confirm model Version 1 is mounted at the exact expected path.
3. Confirm Python 3.12 is used instead of the notebook image default if that default is newer.
4. Export both `LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}` and `LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}` before the first GPU/CUDA probe or FlashInfer cold-JIT path.
5. Read `production/server.pid` and the configured server log when health does not become ready.
6. Do not silently switch back to one T4 and still compare results with the accepted T4x2 baseline.

## Documentation map

The complete bilingual documentation index is [`docs/README.md`](docs/README.md). It links to:

- architecture;
- engineering overview;
- Kaggle setup;
- benchmark methodology and results;
- evidence index;
- reproducibility guide;
- troubleshooting;
- known limitations;
- development history.

## Release assets

The GitHub `v1.0.0` release provides compact reviewer-facing assets rather than duplicating large model/evidence payloads:

- source archive;
- standalone `kaggle-production-showcase.ipynb`;
- machine-readable release manifest;
- `SHA256SUMS.txt`.

Reviewers should treat the annotated Git tag and repository evidence as the release authority, with asset checksums used to verify downloaded copies.

## License

Repository-authored code, scripts, tests, configuration, and documentation are licensed under MIT. See [`LICENSE`](LICENSE) and [`LICENSE-NOTES.md`](LICENSE-NOTES.md).

Boson Higgs TTS 3 model weights and other Higgs Materials are governed by the **Boson Higgs TTS 3 Research and Non-Commercial License**. See the verbatim upstream Agreement at [`LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt`](LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt), the required attribution in [`NOTICE`](NOTICE), and the provenance snapshot in [`LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md`](LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md).

**Built with Higgs TTS 3 licensed from Boson AI USA, Inc.**

Kaggle platform components, SGLang/SGLang-Omni, PyTorch, FlashInfer, and other third-party software remain under their respective licenses and notices. This repository does not grant a commercial license for Higgs TTS 3.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). When referring to benchmark or acceptance claims, cite the exact release/tag and the corresponding retained evidence file rather than quoting only the README summary.

## Project boundary

This repository documents one carefully qualified Kaggle T4x2 deployment and the evidence that supports it. It is intended to make review and reproduction easier, not to overstate model capability.

If a fresh-session rerun disagrees with the retained authority, preserve the conflicting evidence, record the runtime/model/environment differences, and investigate the divergence rather than hiding or normalizing it.
