# Higgs TTS 3 4B on Kaggle T4x2 GPU

[![Repository Audit](https://github.com/dangkhoa2016/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyTorch FP16](https://img.shields.io/badge/PyTorch-FP16-orange.svg)
![SGLang-Omni](https://img.shields.io/badge/SGLang--Omni-0.1.7-blueviolet.svg)
![NVIDIA Tesla T4 x2](https://img.shields.io/badge/GPU-Tesla%20T4%20x2-76B900.svg)
![Kaggle](https://img.shields.io/badge/platform-Kaggle-20BEFF.svg)
![Original weights](https://img.shields.io/badge/weights-original%20%7C%20no%20quantization-success.svg)
![Human listening](https://img.shields.io/badge/core%20TTS-human%20accepted-success.svg)
![Release state](https://img.shields.io/badge/release-pre--v1.0.0-informational.svg)

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

An **independent engineering qualification and deployment project** for running `bosonai/higgs-tts-3-4b` with original weights on Kaggle NVIDIA Tesla T4 x2 GPUs. This repository is **not an official BosonAI release**.

The project preserves both successful results and negative evidence: single-T4 functional inference worked but failed production-headroom qualification, while a T4x2 stage-placement layout recovered memory headroom and completed the accepted warm benchmark.

## Status

- **Core zero-shot TTS packaging:** READY
- **T4x2 warm benchmark baseline:** ACCEPTED
- **English / Vietnamese / EN-VI code-switching core samples:** human-accepted variants available in retained evidence
- **Voice-clone production claim:** PENDING_HUMAN_ACCEPTANCE
- **Current SLT-conditioned reference as production default:** REJECTED
- **Repository release state:** pre-v1.0.0

No v1.0.0 release is claimed until the clean history, remote replacement, and CI gates have completed.

## Accepted T4x2 architecture

```text
CPU   -> preprocessing
GPU0  -> tts_engine
GPU1  -> audio_encoder + vocoder
TP    -> disabled
```

The accepted engine contract uses FP16, CUDA graphs disabled, `max_running_requests=1`, `mem_fraction_static=0.72`, PyTorch sampling, and Triton attention.

A critical fresh-environment requirement observed during qualification is:

```bash
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

This allows the FlashInfer cold-JIT link path to resolve `-lcuda`.

## Model authority

Normal Kaggle execution attaches the existing mirror instead of downloading the model from Hugging Face:

```text
Kaggle model: dangkhoa2016/bosonai-higgs-tts-3-4b
Variation:    transformers/default
Version:      1
Mounted path: /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

The release path uses original weights, FP16 runtime, no GGUF, and no release quantization. Model weights are not stored in this Git repository. Critical model provenance and SHA256 data are retained in [`manifests/`](manifests/).

## Quick start on Kaggle

Use a Kaggle session with two Tesla T4 GPUs and attach the model above. Prepare a Python 3.12 environment matching [`production/requirements-runtime-lock.txt`](production/requirements-runtime-lock.txt), then launch:

```bash
export ROOT="$PWD"
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/serve-t4x2.sh
```

In another shell, verify readiness and run the smoke request:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

For benchmark reruns, use:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

The wrapper writes to a fresh directory by default and the harness protects the retained official benchmark authority from accidental overwrite.

## Official warm benchmark — 2026-10-09

The benchmark used 11 cases x 3 repetitions, sequential requests, and a warm runtime. FlashInfer cold JIT is excluded from the model-generation timing.

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

Ten of eleven cases were immediately byte-identical across the first three repetitions. EN02 diverged on the first observation, then repetitions 2-5 were byte-identical. The retained classification is `FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE`; the cause is **unproven**. This repository does not claim universal bitwise determinism.

See [benchmark methodology](docs/benchmark-methodology.md), [benchmark results](docs/benchmark-results.md), and the machine-readable authority in [`evidence/t4x2-official-benchmark-2026-10-09.json`](evidence/t4x2-official-benchmark-2026-10-09.json).

## Why T4x2 instead of one T4

Single-T4 inference was functionally successful, but Phase 5 recorded only about 65 MiB free on GPU0 after reference/voice-clone use. A later MIX02 request failed with CUDA OOM while the server remained healthy. That failure is retained in [`evidence/phase5-summary.json`](evidence/phase5-summary.json).

The T4x2 stage placement moved the audio encoder and vocoder to GPU1. Phase 6 then returned 5/5 HTTP 200 for the mixed-language suite, including the previously OOM MIX02 case. This is why the project claims a qualified T4x2 baseline rather than a production-safe single-T4 baseline.

## Onset root-cause audit and perceptual acceptance

Historical zero-shot samples showed VI02/MIX02 initial-word loss, MIX03 near-silence, and MIX04 onset behavior. Investigation ruled out tokenizer text loss, delay-pattern off-by-one behavior, codec/HTTP WAV clipping, max-token truncation, and concurrency.

The public classification is:

```text
zero-shot AR acoustic-generation/bootstrap instability before codec decode
confidence: high for layer localization; exact learned-model internal mechanism remains unproven
```

Fixed-seed variants produced accepted VI02, MIX02, and MIX03 outputs. MIX04 was human-approved with seed `12346`, temperature `0.65`, `top_k=50`, `max_new_tokens=384`, followed by `loudnorm=I=-16:TP=-1.5:LRA=7`.

Reference-conditioned SLT output improved onset stability as a diagnostic, but human review found undesirable Vietnamese regional/tone characteristics. It is therefore **diagnostic only**, not the production default.

Voice cloning is runtime-functional with synthetic references, but final perceptual production acceptance remains pending. This project does not use real-person voice cloning for its qualification tests.

## Evidence transparency

The repository intentionally keeps historical negative evidence rather than rewriting it away. Start with:

- [`docs/evidence-index.md`](docs/evidence-index.md) — evidence map and authority hierarchy
- [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json) — current consolidated acceptance status
- [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json) — onset audit
- [`evidence/root-cause-human-review-2026-10-09.json`](evidence/root-cause-human-review-2026-10-09.json) — human-listening decisions
- [`benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json`](benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json) — provenance for omitted bulk raw telemetry

Heavy benchmark WAVs, the 15,339-logical-line raw telemetry file, model weights, `.venv312`, and the captured FlashInfer cache tarball are intentionally excluded from Git.

## Documentation

The complete bilingual documentation index is at [`docs/README.md`](docs/README.md). Key guides include architecture, engineering overview, Kaggle setup, benchmark methodology/results, reproducibility, troubleshooting, known limitations, and development history.

Run the repository audit locally with:

```bash
make verify-final
```

CI runs the same final repository contract without launching model inference.

## License

Repository-authored code, scripts, tests, configuration, and documentation are licensed under MIT: see [`LICENSE`](LICENSE) and [`LICENSE-NOTES.md`](LICENSE-NOTES.md). Model weights and third-party/upstream software remain under their own licenses and notices.

## Project boundary

This repository demonstrates one carefully qualified Kaggle T4x2 configuration. It does not claim universal T4 compatibility, universal request-level byte determinism, a proven exact neural mechanism for onset instability, or production-ready voice cloning.
