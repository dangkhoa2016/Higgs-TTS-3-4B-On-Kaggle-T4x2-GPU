# Evidence Index

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](evidence-index.vi.md)

## Model provenance

- `manifests/model-authority.json` — Kaggle model ID, variation/version, resolved path, file sizes, and safetensors index facts.
- `manifests/model-critical.sha256` — checksums for critical model files; the model safetensors SHA256 ends in the recorded authority value `...f8ae3d5a`.

## Historical runtime phases

- `evidence/phase3-summary.json` — first successful single-T4 FP16 TTS and FlashInfer cold-JIT link finding.
- `evidence/phase4-summary.json` — functional language/control transport plus historical perceptual review.
- `evidence/phase5-summary.json` — single-T4 `FAIL_PRODUCTION_HEADROOM`, including MIX02 CUDA OOM.
- `evidence/phase6-summary.json` — accepted T4x2 stage placement and 5/5 mixed-language HTTP recovery.
- `evidence/phase6-resolved-config-v2.txt` — retained resolved runtime/config snapshot.

These historical files are preserved rather than rewritten to match later perceptual decisions.

## Root-cause and human review

- `evidence/root-cause-audit-2026-10-09.json` — localization of the onset issue before codec decode, ruled-out layers, fixed-seed diagnostics, and confidence wording.
- `evidence/root-cause-human-review-2026-10-09.json` — human listening conclusions, including rejection of the current SLT-conditioned voice as production default.
- `evidence/mix04-final-approved.json` — final MIX04 human-approved seed/temperature/post-processing authority.
- `evidence/final-acceptance-matrix-2026-10-09.json` — consolidated current perceptual/readiness status while explicitly preserving historical failures.

## Official benchmark

- `evidence/t4x2-official-benchmark-2026-10-09.json` — compact benchmark authority and accepted verdict.
- `benchmarks/t4x2-official-2026-10-09/benchmark-meta.json` — runtime snapshot and protocol metadata.
- `benchmarks/t4x2-official-2026-10-09/summary.json` — per-case and aggregate statistics.
- `benchmarks/t4x2-official-2026-10-09/en02-extra-repro.json` — EN02 repetitions 4 and 5.
- `benchmarks/t4x2-official-2026-10-09/postprocess-summary.json` — MIX04 loudness-normalization timing.
- `benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json` — checksum/size/line metadata for the intentionally omitted raw telemetry file.

Benchmark WAVs, `results.partial.json`, and the 15,339-logical-line raw `results.json` are not committed to the source repository. The public claims above rely on the compact retained authority files.

## Smoke authority

`evidence/production-smoke-2026-10-09.json` records the packaged runtime smoke result: HTTP 200, 24 kHz mono audio, positive duration, and output checksum.

## Reading status correctly

The final acceptance matrix supersedes the current perceptual status of earlier phase summaries; it does not erase or modify those historical records. Voice-clone production acceptance remains pending.
