# Kết quả benchmark

> 🌐 Ngôn ngữ / Language: [English](benchmark-results.md) | **Tiếng Việt**

## Official warm baseline

Authority: `evidence/t4x2-official-benchmark-2026-10-09.json`.

| Metric | Kết quả |
| --- | ---: |
| Cases | 11 |
| Repetitions mỗi case | 3 |
| Measured requests | 33 |
| HTTP 200 | 33 / 33 |
| Mean latency | 6.013801 s |
| Median latency | 5.979205 s |
| p95 latency | 7.094262 s |
| Mean RTF | 1.087838 |
| Aggregate RTF | 1.086832 |
| Aggregate audio | 182.6 s |
| Aggregate wall time | 198.455444 s |
| GPU0 peak used | 10,951 MiB |
| GPU1 peak used | 4,511 MiB |

Cách diễn giải được chấp nhận là: warm runtime PASS, stage-placement memory headroom PASS, latency/RTF reproducibility PASS và production benchmark baseline ACCEPTED.

## Bitwise reproducibility

Mười trên mười một case byte-identical trong ba benchmark repetitions đầu.

EN02 là ngoại lệ. Run đầu tạo artifact 6.80 s với SHA256 bắt đầu `d222da...`; runs 2 và 3 tạo artifact 6.24 s với SHA256 bắt đầu `7b160c...`. Hai run bổ sung 4 và 5 khớp chính xác với hash thứ hai.

Classification được giữ lại:

```text
FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE
cause: unproven
```

Vì vậy repository không claim mọi request đều universally bitwise deterministic.

## MIX04 post-processing

MIX04 accepted variant dùng seed 12346, temperature 0.65 và loudness normalization. Benchmark normalization được tách khỏi model-generation timing. Mean đã đo xấp xỉ 0.316 s trên năm post-processing runs.

## Lưu raw results

Raw per-request telemetry 313,295 byte chủ ý không đưa vào Git source tree vì khi biểu diễn text có 15,339 logical lines. `benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json` ghi SHA256, byte size, line accounting, retained authority path và lý do loại khỏi Git.
