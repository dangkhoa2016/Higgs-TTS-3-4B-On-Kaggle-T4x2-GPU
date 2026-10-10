# Development History

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](development-history.vi.md)

This history separates evidence-backed engineering milestones from the pre-publication clean-history assembly. Related files may be folded into the focused commit that represents their reviewable concern before the first community publication; retained evidence timestamps remain the authority for experiment/runtime chronology.

## 2026-10-08 — model and runtime qualification

The project used the existing Kaggle mirror `dangkhoa2016/bosonai-higgs-tts-3-4b`, original model weights, and an FP16 SGLang-Omni runtime. A single Tesla T4 successfully produced speech after the FlashInfer cold-JIT link path was corrected with `LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}` plus `LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}`.

Functional validation exercised English, Vietnamese, control tokens, mixed-language prompts, and synthetic-reference voice-clone transport. Human review also identified real perceptual failures: VI02 lost its initial word, MIX02 lost its initial word, MIX03 was near-silent, MIX04 lost its initial English word, and the original synthetic voice-clone reference sounded too low/heavy.

## 2026-10-08 — single-T4 headroom failure and T4x2 recovery

single-T4 headroom qualification preserved a production-headroom failure: after warm/reference use GPU0 had almost no free memory and MIX02 hit CUDA OOM. This became negative evidence rather than a result to hide.

T4x2 stage-placement qualification moved `audio_encoder` and `vocoder` to GPU1 while keeping `tts_engine` on GPU0 and preprocessing on CPU. Tensor parallelism remained disabled. The five-case mixed-language suite then returned 5/5 HTTP 200 and recovered the previously OOM MIX02 case.

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

## 2026-10-09 — Kaggle production showcase and first public release

The repository added an importable Kaggle T4x2 production showcase notebook so reviewers can start from the GitHub release, attach the existing Kaggle model mirror, run the real service, listen to multilingual acceptance outputs, and rerun the official benchmark from a fresh session. The notebook verifies the annotated `v1.0.0` tag resolves to the checked-out HEAD rather than embedding a self-referential commit hash.

After the clean-history branch passed local repository verification and GitHub Actions, annotated tag `v1.0.0` became the first public release boundary. Voice-clone production acceptance remains pending; the release does not elevate that unresolved perceptual claim.
