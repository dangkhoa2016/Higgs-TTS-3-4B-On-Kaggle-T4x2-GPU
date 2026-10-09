# Architecture

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](architecture.vi.md)

## Accepted baseline

The accepted production baseline uses stage placement across two Kaggle NVIDIA Tesla T4 GPUs rather than tensor parallelism.

```text
CPU   -> preprocessing
GPU0  -> tts_engine
GPU1  -> audio_encoder + vocoder
TP    -> disabled
```

This layout is recorded in `evidence/t4x2-stage-placement-validation.json` and implemented by `production/serve-t4x2.sh`.

## Why this layout exists

Single-T4 inference proved functional, but after warmup/reference use the remaining VRAM was too small for some eager codec decode allocations. `evidence/single-t4-production-headroom.json` records MIX02 failing with CUDA OOM while the server remained healthy.

Moving the audio encoder and vocoder to GPU1 reduced steady GPU0 pressure while keeping the TTS engine on GPU0. The T4x2 stage-placement qualification mixed-language suite then returned 5/5 HTTP 200 responses, including the previously OOM MIX02 case.

## Engine contract

The qualified TTS engine uses FP16, CUDA graphs disabled, one running request, `mem_fraction_static=0.72`, PyTorch sampling, and Triton attention. The server exports:

```bash
LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

That environment path is required for the observed FlashInfer cold-JIT link path to resolve `-lcuda`.

## Model boundary

The model is mounted separately from Kaggle at `/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1`. No model weights are committed to this repository, and the accepted release path uses original weights without GGUF or release quantization.

## Scope

This architecture is a qualified Kaggle T4x2 baseline. It is not a claim of universal compatibility with all T4 systems, driver stacks, or workload shapes.
