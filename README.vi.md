# Higgs TTS 3 4B trên Kaggle T4x2 GPU

[![Repository Audit](https://github.com/dangkhoa2016/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyTorch FP16](https://img.shields.io/badge/PyTorch-FP16-orange.svg)
![SGLang-Omni](https://img.shields.io/badge/SGLang--Omni-0.1.7-blueviolet.svg)
![NVIDIA Tesla T4 x2](https://img.shields.io/badge/GPU-Tesla%20T4%20x2-76B900.svg)
![Kaggle](https://img.shields.io/badge/platform-Kaggle-20BEFF.svg)
![Original weights](https://img.shields.io/badge/weights-original%20%7C%20no%20quantization-success.svg)
![Human listening](https://img.shields.io/badge/core%20TTS-human%20accepted-success.svg)
![Release state](https://img.shields.io/badge/release-pre--v1.0.0-informational.svg)

> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**

Một **dự án độc lập về kiểm định kỹ thuật và triển khai** để chạy `bosonai/higgs-tts-3-4b` bằng original weights trên GPU NVIDIA Tesla T4 x2 của Kaggle. Repository này **không phải bản phát hành chính thức của BosonAI**.

Project giữ cả kết quả thành công lẫn negative evidence: inference trên single-T4 chạy được về mặt chức năng nhưng fail production-headroom qualification, trong khi layout stage-placement T4x2 phục hồi memory headroom và hoàn tất accepted warm benchmark.

## Trạng thái

- **Core zero-shot TTS packaging:** READY
- **T4x2 warm benchmark baseline:** ACCEPTED
- **Core English / Vietnamese / EN-VI code-switching samples:** có human-accepted variants trong retained evidence
- **Voice-clone production claim:** PENDING_HUMAN_ACCEPTANCE
- **Current SLT-conditioned reference làm production default:** REJECTED
- **Repository release state:** pre-v1.0.0

Không claim đã có v1.0.0 release cho đến khi clean history, remote replacement và CI gates hoàn tất.

## Kiến trúc T4x2 được chấp nhận

```text
CPU   -> preprocessing
GPU0  -> tts_engine
GPU1  -> audio_encoder + vocoder
TP    -> disabled
```

Accepted engine contract dùng FP16, tắt CUDA graphs, `max_running_requests=1`, `mem_fraction_static=0.72`, PyTorch sampling và Triton attention.

Một fresh-environment requirement quan trọng đã quan sát trong qualification là:

```bash
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

Điều này cho phép FlashInfer cold-JIT link path resolve `-lcuda`.

## Model authority

Normal Kaggle execution attach mirror hiện có thay vì download model từ Hugging Face:

```text
Kaggle model: dangkhoa2016/bosonai-higgs-tts-3-4b
Variation:    transformers/default
Version:      1
Mounted path: /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

Release path dùng original weights, runtime FP16, không GGUF và không release quantization. Model weights không được lưu trong Git repository này. Critical model provenance và SHA256 data được giữ tại [`manifests/`](manifests/).

## Quick start trên Kaggle

Dùng Kaggle session có hai Tesla T4 và attach model ở trên. Chuẩn bị môi trường Python 3.12 khớp [`production/requirements-runtime-lock.txt`](production/requirements-runtime-lock.txt), sau đó launch:

```bash
export ROOT="$PWD"
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/serve-t4x2.sh
```

Ở shell khác, verify readiness và chạy smoke request:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

Để rerun benchmark, dùng:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

Wrapper mặc định ghi vào fresh directory và harness bảo vệ retained official benchmark authority khỏi accidental overwrite.

## Official warm benchmark — 2026-10-09

Benchmark dùng 11 cases x 3 repetitions, requests chạy tuần tự và warm runtime. FlashInfer cold JIT không được tính trong model-generation timing.

| Metric | Kết quả |
| --- | ---: |
| HTTP success | **33 / 33** |
| Mean latency | **6.013801 s** |
| Median latency | **5.979205 s** |
| p95 latency | **7.094262 s** |
| Mean RTF | **1.087838** |
| Aggregate RTF | **1.086832** |
| Aggregate audio | **182.6 s** |
| Aggregate wall | **198.455444 s** |
| GPU0 peak used | **10,951 MiB** |
| GPU1 peak used | **4,511 MiB** |

Mười trên mười một case byte-identical ngay trong ba repetitions đầu. EN02 diverge ở first observation, sau đó repetitions 2-5 byte-identical. Classification được giữ là `FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE`; cause **unproven**. Repository không claim universal bitwise determinism.

Xem [benchmark methodology](docs/benchmark-methodology.vi.md), [benchmark results](docs/benchmark-results.vi.md) và machine-readable authority tại [`evidence/t4x2-official-benchmark-2026-10-09.json`](evidence/t4x2-official-benchmark-2026-10-09.json).

## Vì sao dùng T4x2 thay vì một T4

Single-T4 inference chạy thành công về mặt chức năng, nhưng Phase 5 ghi chỉ còn khoảng 65 MiB free trên GPU0 sau reference/voice-clone use. Một MIX02 request về sau bị CUDA OOM trong khi server vẫn healthy. Failure đó được giữ trong [`evidence/phase5-summary.json`](evidence/phase5-summary.json).

T4x2 stage placement chuyển audio encoder và vocoder sang GPU1. Phase 6 sau đó trả 5/5 HTTP 200 cho mixed-language suite, gồm cả MIX02 trước đó bị OOM. Đây là lý do project claim qualified T4x2 baseline thay vì production-safe single-T4 baseline.

## Onset root-cause audit và perceptual acceptance

Historical zero-shot samples có VI02/MIX02 initial-word loss, MIX03 near-silence và MIX04 onset behavior. Investigation loại trừ tokenizer text loss, delay-pattern off-by-one, codec/HTTP WAV clipping, max-token truncation và concurrency.

Public classification là:

```text
zero-shot AR acoustic-generation/bootstrap instability before codec decode
confidence: high for layer localization; exact learned-model internal mechanism remains unproven
```

Fixed-seed variants tạo accepted VI02, MIX02 và MIX03 outputs. MIX04 được human approval với seed `12346`, temperature `0.65`, `top_k=50`, `max_new_tokens=384`, sau đó `loudnorm=I=-16:TP=-1.5:LRA=7`.

Reference-conditioned SLT output cải thiện onset stability ở diagnostic, nhưng human review phát hiện Vietnamese regional/tone characteristics không mong muốn. Vì vậy nó **chỉ dùng diagnostic**, không phải production default.

Voice cloning hoạt động về runtime với synthetic references, nhưng final perceptual production acceptance vẫn pending. Project không dùng real-person voice cloning cho qualification tests.

## Minh bạch evidence

Repository chủ ý giữ historical negative evidence thay vì rewrite cho đẹp hơn. Bắt đầu từ:

- [`docs/evidence-index.vi.md`](docs/evidence-index.vi.md) — evidence map và authority hierarchy
- [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json) — current consolidated acceptance status
- [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json) — onset audit
- [`evidence/root-cause-human-review-2026-10-09.json`](evidence/root-cause-human-review-2026-10-09.json) — human-listening decisions
- [`benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json`](benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json) — provenance cho bulk raw telemetry được loại khỏi Git

Heavy benchmark WAVs, raw telemetry file 15,339 logical lines, model weights, `.venv312` và captured FlashInfer cache tarball đều chủ ý không đưa vào Git.

## Tài liệu

Complete bilingual documentation index nằm tại [`docs/README.vi.md`](docs/README.vi.md). Các guide chính gồm architecture, engineering overview, Kaggle setup, benchmark methodology/results, reproducibility, troubleshooting, known limitations và development history.

Chạy repository audit local bằng:

```bash
make verify-final
```

CI chạy cùng final repository contract mà không launch model inference.

## License

Repository-authored code, scripts, tests, configuration và documentation dùng MIT: xem [`LICENSE`](LICENSE) và [`LICENSE-NOTES.vi.md`](LICENSE-NOTES.vi.md). Model weights và third-party/upstream software vẫn tuân theo licenses/notices riêng.

## Ranh giới project

Repository này chứng minh một cấu hình Kaggle T4x2 được kiểm định kỹ. Nó không claim universal T4 compatibility, universal request-level byte determinism, exact neural mechanism đã được chứng minh cho onset instability hoặc production-ready voice cloning.
