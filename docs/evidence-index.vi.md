# Chỉ mục evidence

> 🌐 Ngôn ngữ / Language: [English](evidence-index.md) | **Tiếng Việt**

## Model provenance

- `manifests/model-authority.json` — Kaggle model ID, variation/version, resolved path, file sizes và safetensors index facts.
- `manifests/model-critical.sha256` — checksum của các model file quan trọng; model safetensors SHA256 kết thúc bằng authority value đã ghi `...f8ae3d5a`.

## Evidence qualification runtime lịch sử

- `evidence/single-t4-first-tts.json` — single-T4 FP16 TTS thành công đầu tiên và FlashInfer cold-JIT link finding.
- `evidence/functional-language-control-validation.json` — functional language/control transport cùng historical perceptual review.
- `evidence/single-t4-production-headroom.json` — single-T4 `FAIL_PRODUCTION_HEADROOM`, bao gồm MIX02 CUDA OOM.
- `evidence/t4x2-stage-placement-validation.json` — accepted T4x2 stage placement và mixed-language HTTP recovery 5/5.
- `evidence/t4x2-resolved-runtime-config.txt` — retained resolved runtime/config snapshot.

Các retained record này giữ nguyên kết quả qualification đã quan sát nhưng dùng reviewer-facing naming.

## Root-cause và human review

- `evidence/root-cause-audit-2026-10-09.json` — định vị onset issue trước codec decode, các layer đã loại trừ, fixed-seed diagnostics và confidence wording.
- `evidence/root-cause-human-review-2026-10-09.json` — kết luận human listening, bao gồm việc reject current SLT-conditioned voice làm production default.
- `evidence/mix04-final-approved.json` — authority cho MIX04 final human-approved seed/temperature/post-processing.
- `evidence/final-acceptance-matrix-2026-10-09.json` — consolidated current perceptual/readiness status nhưng vẫn giữ nguyên historical failures.
- `evidence/kaggle-showcase-human-review-nonofficial-account-2026-10-10.json` — historical human listening approval cho reviewer showcase 8 case và 4 synthetic reference preview từ một run trên Kaggle account không phải tài khoản chính thức của project owner; official project-owner run về sau hiện có machine acceptance và human-reviewed perceptual acceptance riêng.

- `evidence/kaggle-official-account-execution-2026-10-10.json` — execution từ Kaggle account chính thức của project owner, scriptVersionId `356925390`; machine acceptance PASS và linked human-reviewed perceptual acceptance PASS.
- `evidence/kaggle-official-account-human-review-2026-10-10.json` — human listening review của fresh official Output; perceptual acceptance PASS, với MIX04 được giữ minh bạch dưới dạng accepted known low-raw-loudness evidence.

## Official benchmark

- `evidence/t4x2-official-benchmark-2026-10-09.json` — compact benchmark authority và accepted verdict.
- `benchmarks/t4x2-official-2026-10-09/benchmark-meta.json` — runtime snapshot và protocol metadata.
- `benchmarks/t4x2-official-2026-10-09/summary.json` — per-case và aggregate statistics.
- `benchmarks/t4x2-official-2026-10-09/en02-extra-repro.json` — EN02 repetitions 4 và 5.
- `benchmarks/t4x2-official-2026-10-09/postprocess-summary.json` — MIX04 loudness-normalization timing.
- `benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json` — checksum/size/line metadata của raw telemetry file chủ ý không commit.

Benchmark WAVs, `results.partial.json` và raw `results.json` có 15,339 logical lines không được commit vào source repository. Public claims ở trên dựa trên compact retained authority files.

## Smoke authority

`evidence/production-smoke-2026-10-09.json` ghi packaged runtime smoke result: HTTP 200, audio mono 24 kHz, duration dương và output checksum.

## Cách đọc status đúng

Final acceptance matrix supersede current perceptual status của earlier qualification summaries; nó không xóa hoặc sửa các historical records đó. Voice-clone production acceptance vẫn pending.
