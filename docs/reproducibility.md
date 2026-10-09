# Reproducibility

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](reproducibility.vi.md)

## Reproduce the qualified environment

Attach Kaggle model `dangkhoa2016/bosonai-higgs-tts-3-4b`, variation `transformers/default`, version `1`, and use a T4x2 session. The expected model path and full captured Python package set are documented in `production/runtime.env` and `production/requirements-runtime-lock.txt`.

Verify the critical model checksums against `manifests/model-critical.sha256` before comparing results across machines.

## Launch the accepted baseline

```bash
export ROOT="$PWD"
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/serve-t4x2.sh
```

In another shell, run:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

The accepted placement is CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder, with tensor parallelism disabled.

## Rerun the benchmark safely

Do not target the retained `benchmarks/t4x2-official-2026-10-09/` directory. The wrapper generates a fresh timestamped destination when no path is supplied:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

A custom fresh directory may be passed as the first argument.

## What should reproduce

The official authority demonstrates 33/33 HTTP 200 requests and stable latency/RTF behavior for the qualified warm baseline. Ten of eleven cases were byte-identical across their first three repetitions.

Fixed seeds and a pinned runtime make comparison stronger, but they do not establish universal byte determinism. EN02's first observation differed and then repetitions 2-5 stabilized to one byte-identical result. The cause is explicitly unproven.

## Warm versus cold behavior

The official benchmark excludes FlashInfer cold JIT. A fresh machine may compile FlashInfer operators before warm behavior is reached. The observed `-lcuda` link failure is addressed by `LD_LIBRARY_PATH` plus `LIBRARY_PATH`; an optional external cache can accelerate migration but is not part of the Git source release.

## Perceptual reproducibility

The repository records human-approved variants for core TTS cases, but audio quality remains a perceptual property rather than a checksum-only claim. Voice-clone runtime functionality must not be interpreted as final production perceptual acceptance.
