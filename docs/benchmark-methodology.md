# Benchmark Methodology

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](benchmark-methodology.vi.md)

## Purpose

The official benchmark characterizes the accepted warm Kaggle T4x2 stage-placement baseline. It is not a cold-start benchmark and does not include FlashInfer JIT compilation time.

## Runtime layout

- CPU: preprocessing
- GPU0: `tts_engine`
- GPU1: `audio_encoder` + `vocoder`
- Tensor parallelism: disabled
- `max_running_requests=1`
- Requests: sequential

## Workload

The harness defines 11 prompts: three English, three Vietnamese, and five EN-VI code-switching cases. Each case runs three repetitions, for 33 measured requests total.

Before those measurements, one warmup request is executed and excluded from the 33-request performance summary.

## Sampling contract

Ten cases use:

```text
seed=12345
temperature=0.8
top_k=50
max_new_tokens=384
```

MIX04 uses its human-approved generation settings:

```text
seed=12346
temperature=0.65
top_k=50
max_new_tokens=384
```

## Measurements

For each request the harness records wall time, generated audio duration, real-time factor (RTF), output SHA256, and periodic GPU memory/utilization samples. The summary aggregates latency, RTF, audio/wall totals, GPU memory peaks, and per-case hash reproducibility.

## Post-processing boundary

MIX04's accepted loudness normalization uses `loudnorm=I=-16:TP=-1.5:LRA=7`. Its post-processing benchmark is recorded separately and is **not** included in model-generation latency or RTF.

## Reproducibility interpretation

Fixed seeds support comparable reruns, but the evidence does not justify claiming universal byte determinism. Ten of eleven cases were immediately byte-identical across the first three repetitions. EN02's first observation differed, while repetitions 2-5 were byte-identical; the cause remains unproven.

## Authority protection

The public benchmark wrapper writes to a fresh output directory by default. The retained `benchmarks/t4x2-official-2026-10-09/` authority is protected from accidental overwrite by the harness.
