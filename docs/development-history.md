# Development History

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](development-history.vi.md)

This history separates evidence-backed engineering milestones from the later public Git-history rewrite. Dates below describe retained project activity; the clean rewrite commits use their actual rewrite timestamps and are not backdated to imitate earlier development.

## 2026-10-08 — model and runtime qualification

The project used the existing Kaggle mirror `dangkhoa2016/bosonai-higgs-tts-3-4b`, original model weights, and an FP16 SGLang-Omni runtime. A single Tesla T4 successfully produced speech after the FlashInfer cold-JIT link path was corrected with `LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}`.

Functional validation exercised English, Vietnamese, control tokens, mixed-language prompts, and synthetic-reference voice-clone transport. Human review also identified real perceptual failures: VI02 lost its initial word, MIX02 lost its initial word, MIX03 was near-silent, MIX04 lost its initial English word, and the original synthetic voice-clone reference sounded too low/heavy.

## 2026-10-08 — single-T4 headroom failure and T4x2 recovery

Phase 5 preserved a production-headroom failure: after warm/reference use GPU0 had almost no free memory and MIX02 hit CUDA OOM. This became negative evidence rather than a result to hide.

Phase 6 moved `audio_encoder` and `vocoder` to GPU1 while keeping `tts_engine` on GPU0 and preprocessing on CPU. Tensor parallelism remained disabled. The five-case mixed-language suite then returned 5/5 HTTP 200 and recovered the previously OOM MIX02 case.

## 2026-10-09 — onset root-cause audit and perceptual acceptance

Static and raw-code audits ruled out tokenizer text loss, delay-pattern off-by-one behavior, codec/WAV assembly clipping, max-token truncation, and request concurrency as the source of the onset failures. Raw-code re-decode and API WAV output correlated at approximately 0.9999998 or higher.

The retained classification is `zero-shot AR acoustic-generation/bootstrap instability before codec decode`, with high confidence for layer localization while the exact learned-model internal mechanism remains unproven.

Fixed-seed zero-shot variants improved the affected cases. The SLT-conditioned diagnostic improved onset stability but introduced undesirable Vietnamese regional/tone characteristics and was rejected as the production default. MIX04 was finally human-approved at seed 12346, temperature 0.65, followed by loudness normalization.

## 2026-10-09 — production packaging and official warm benchmark

Production helpers, readiness checks, smoke validation, runtime lock data, and a migration bundle were prepared. The official warm T4x2 benchmark ran 11 cases x 3 repetitions sequentially: 33/33 HTTP 200, mean latency about 6.014 s, aggregate RTF about 1.086832, and GPU peaks of 10,951/4,511 MiB.

Ten of eleven cases were immediately byte-stable across the first three repetitions. EN02 diverged on its first observation and then produced four consecutive byte-identical results; the cause remains unproven.

## 2026-10-09 — clean public-history rebuild

An initial GitHub publication was rejected because its commits were created seconds apart and looked like a bulk import. The repository was therefore rebuilt from a clean root using the retained engineering authority, small reviewable commits, bilingual documentation, MIT licensing, governance, tests, CI, and explicit preservation of failures.

The rewrite does not fabricate historical commit timestamps. Historical engineering dates live in this document and retained evidence; Git commits record when the rewrite work actually occurred.

## Current release boundary

The clean branch is still pre-v1.0.0 until local history verification, protected remote replacement, and GitHub Actions verification succeed. Voice-clone production acceptance remains pending.
