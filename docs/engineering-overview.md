# Engineering Overview

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](engineering-overview.vi.md)

## Objective

Qualify BosonAI Higgs TTS 3 4B on Kaggle Tesla T4 hardware using the original Kaggle-mounted weights, with transparent evidence for both successes and failures.

## Qualification progression

1. The model authority and runtime stack were identified and pinned.
2. A single T4 loaded the model and produced successful FP16 TTS output.
3. English, Vietnamese, control-token, mixed-language, and synthetic-reference transport paths were exercised.
4. Production-headroom testing exposed a real single-T4 limit: MIX02 eventually failed with CUDA OOM after the pipeline was fully warm.
5. T4x2 stage placement moved the audio encoder and vocoder to GPU1 while leaving the TTS engine on GPU0.
6. The T4x2 mixed suite recovered the previously failing case and established the accepted runtime baseline.
7. An onset audit localized historical VI02/MIX02/MIX03/MIX04 behavior to zero-shot autoregressive acoustic generation before codec decode, with the exact learned internal mechanism intentionally left unproven.
8. Fixed-seed variants and the final MIX04 seed/temperature choice were reviewed by human listening.
9. The official warm benchmark completed 33/33 HTTP 200 requests and became the performance authority for this repository.

## What is production-ready here

The core zero-shot TTS packaging and the T4x2 warm benchmark baseline are accepted. English, Vietnamese, code-switching, and control examples have human-accepted variants.

Voice cloning is different: runtime transport is functional, but the project has not granted final perceptual production acceptance to the synthetic-reference clone path. The repository therefore does not claim production-ready voice cloning.

## Evidence-first policy

Historical Phase 4/5/6 JSON remains unchanged. The consolidated final acceptance matrix records the latest perceptual decisions while explicitly preserving earlier failures. This prevents a later README or release note from erasing the engineering path that led to the accepted baseline.
