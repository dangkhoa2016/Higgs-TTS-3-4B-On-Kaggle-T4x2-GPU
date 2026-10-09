# Phương pháp benchmark

> 🌐 Ngôn ngữ / Language: [English](benchmark-methodology.md) | **Tiếng Việt**

## Mục đích

Official benchmark đặc tả accepted warm Kaggle T4x2 stage-placement baseline. Đây không phải cold-start benchmark và không tính thời gian FlashInfer JIT compilation.

## Runtime layout

- CPU: preprocessing
- GPU0: `tts_engine`
- GPU1: `audio_encoder` + `vocoder`
- Tensor parallelism: disabled
- `max_running_requests=1`
- Requests: sequential

## Workload

Harness định nghĩa 11 prompt: ba English, ba Vietnamese và năm EN-VI code-switching. Mỗi case chạy ba repetitions, tổng cộng 33 measured requests.

Trước phần đo này có một warmup request và request đó không được tính vào performance summary 33 request.

## Sampling contract

Mười case dùng:

```text
seed=12345
temperature=0.8
top_k=50
max_new_tokens=384
```

MIX04 dùng generation settings đã được human approval:

```text
seed=12346
temperature=0.65
top_k=50
max_new_tokens=384
```

## Phép đo

Với mỗi request, harness ghi wall time, generated audio duration, real-time factor (RTF), output SHA256 và GPU memory/utilization samples theo chu kỳ. Summary tổng hợp latency, RTF, audio/wall totals, GPU memory peaks và per-case hash reproducibility.

## Ranh giới post-processing

MIX04 dùng loudness normalization `loudnorm=I=-16:TP=-1.5:LRA=7`. Post-processing benchmark được ghi riêng và **không** nằm trong model-generation latency hoặc RTF.

## Cách hiểu reproducibility

Fixed seeds hỗ trợ rerun có thể so sánh, nhưng evidence không đủ để claim universal byte determinism. Mười trên mười một case byte-identical ngay trong ba repetitions đầu. EN02 có first observation khác, còn repetitions 2-5 byte-identical; cause vẫn unproven.

## Bảo vệ authority

Public benchmark wrapper mặc định ghi vào output directory mới. Authority `benchmarks/t4x2-official-2026-10-09/` được harness bảo vệ khỏi accidental overwrite.
