# T4x2 Official Warm Benchmark — 2026-10-09

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This directory is the compact, reviewable benchmark authority for the accepted Higgs TTS 3 4B Kaggle T4x2 baseline. It is evidence, not runtime code: the files here explain the conditions, measurements, reproducibility observations, and provenance behind the performance numbers quoted by the repository and release.

For the executable workflow, use [`../../notebooks/kaggle-production-showcase.ipynb`](../../notebooks/kaggle-production-showcase.ipynb) and the benchmark harness in [`../../scripts/benchmark_t4x2_official.py`](../../scripts/benchmark_t4x2_official.py).

## What this benchmark establishes

The retained warm benchmark used the accepted stage placement:

- CPU: preprocessing
- GPU0: `tts_engine`
- GPU1: `audio_encoder + vocoder`
- tensor parallelism: disabled
- requests: sequential
- fixed seed per case
- repetitions: 3 per case
- cases: 11
- measured requests: 33
- HTTP 200: 33 / 33

FlashInfer cold JIT is intentionally excluded from warm timing. Cold-start behavior is documented separately in the repository evidence.

## Frozen baseline results

| Metric | Retained result |
| --- | ---: |
| Mean latency | 6.013801 s |
| Median latency | 5.979205 s |
| p95 latency | 7.094262 s |
| Mean RTF | 1.087838 |
| Aggregate RTF | 1.086832 |
| Aggregate generated audio | 182.6 s |
| Aggregate wall time | 198.455444 s |
| GPU0 peak used | 10,951 MiB |
| GPU1 peak used | 4,511 MiB |

RTF is wall time divided by generated-audio duration. An RTF near 1 means approximately one second of compute wall time per second of generated audio for this sequential benchmark profile.

These numbers are a **frozen official baseline**. They should not be silently replaced by values from later notebook reruns, because generated duration, runtime state, or other execution details can differ between runs. A later fresh-release acceptance run is a validation of the published release path; it is not automatically a replacement for this benchmark authority.

## File map

### `benchmark-meta.json`

Defines the benchmark context before measurement: health state, T4x2 placement, GPU memory state, repetition count, telemetry sampling interval, and warm/cold policy.

### `summary.json`

The primary machine-readable benchmark summary. It contains overall performance, per-case latency/RTF statistics, GPU peaks, generated-audio durations, and SHA-256 values for each repetition.

### `en02-extra-repro.json`

Preserves the additional EN02 investigation. EN02 differed on its first observation, while repetitions 2 through 5 converged to the same 6.24-second, byte-identical output. The exact cause is not claimed; it remains unproven.

### `postprocess-summary.json`

Records the separately measured MIX04 loudness-normalization post-processing cost. Post-processing time is not included in model-generation latency.

### `RAW-RESULTS-PROVENANCE.json`

Records provenance for the omitted raw `results.json`. The original raw telemetry contains 15,339 logical lines and is intentionally not committed to the Git source tree. Its SHA-256, byte size, authority path, and omission reason are retained here so the public claims still have an auditable provenance chain.

## Reproducibility interpretation

Ten of the eleven cases were byte-identical across their first three benchmark repetitions. EN02 was not: its first observation differed, while repetitions 2–5 were byte-identical. Therefore this benchmark does **not** claim universal bitwise determinism.

What it does support is:

- successful warm T4x2 runtime across all 33 measured requests;
- stable sequential latency/RTF for the retained benchmark profile;
- accepted T4x2 stage-placement memory headroom;
- transparent retention of the EN02 first-observation anomaly instead of hiding it.

See [`../../evidence/t4x2-official-benchmark-2026-10-09.json`](../../evidence/t4x2-official-benchmark-2026-10-09.json) for the compact public verdict and acceptance classification.

## Why the raw telemetry and WAVs are not in Git

The source repository is intentionally kept lightweight. Bulk per-request telemetry, generated WAV files, model weights, runtime virtual environments, and transient caches are not source artifacts and are not duplicated into Git.

The omission is explicit rather than silent: `RAW-RESULTS-PROVENANCE.json` preserves the raw-result checksum and size, while the committed summary/evidence files retain the public benchmark claims needed for review.

## How community reviewers should use this directory

Use this snapshot to answer four questions:

1. **What exactly was benchmarked?** Read `benchmark-meta.json`.
2. **What performance was measured?** Read `summary.json`.
3. **Were anomalous observations hidden?** Inspect `en02-extra-repro.json` and the per-case hashes.
4. **Where are the omitted raw results accounted for?** Read `RAW-RESULTS-PROVENANCE.json`.

For a fresh end-to-end release check, run the Kaggle production showcase notebook. Treat its newly generated acceptance evidence as a fresh validation run and this directory as the frozen official benchmark baseline used by the release documentation.
