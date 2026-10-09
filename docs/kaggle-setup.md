# Kaggle Setup

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](kaggle-setup.vi.md)

## Hardware and model attachment

Use a Kaggle notebook/session with two NVIDIA Tesla T4 GPUs and attach the existing Kaggle model mirror:

```text
dangkhoa2016/bosonai-higgs-tts-3-4b
variation: transformers/default
version: 1
```

The expected mounted model path is:

```text
/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

Normal production execution does not download the model from Hugging Face.

## Runtime environment

The qualified environment recorded Python 3.12.3, PyTorch 2.13.0+cu130, SGLang 0.5.20, SGLang-Omni 0.1.7, and FlashInfer 0.6.18. `production/requirements-runtime-lock.txt` preserves the full captured package set.

Before launch, make sure the CUDA driver library path is available:

```bash
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

## Launch

From the repository root:

```bash
export ROOT="$PWD"
bash production/serve-t4x2.sh
```

For background execution:

```bash
export ROOT="$PWD"
bash production/start-background.sh
```

The accepted layout is CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder, with tensor parallelism disabled.

## Readiness and smoke validation

With the service running:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

The smoke helper requires HTTP 200, 24 kHz mono WAV output, and positive duration. It does not expose a public tunnel.

## FlashInfer cache

`production/restore-flashinfer-cache.sh` supports an optional preserved FlashInfer cache when supplied externally. The cache tarball is intentionally not committed to Git. If it is absent, the helper exits cleanly and the environment may perform cold JIT compilation.

## Benchmark reruns

Run benchmarks only after readiness passes. The wrapper creates a fresh output directory by default so the retained official 2026-10-09 authority cannot be overwritten accidentally.
