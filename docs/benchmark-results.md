# Benchmark Results

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](benchmark-results.vi.md)

## Official warm baseline

Authority: `evidence/t4x2-official-benchmark-2026-10-09.json`.

| Metric | Result |
| --- | ---: |
| Cases | 11 |
| Repetitions per case | 3 |
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

The accepted interpretation is: warm runtime PASS, stage-placement memory headroom PASS, latency/RTF reproducibility PASS, and the production benchmark baseline ACCEPTED.

## Bitwise reproducibility

Ten of eleven cases were byte-identical across the first three benchmark repetitions.

EN02 was the exception. Its first run produced a 6.80 s artifact with SHA256 beginning `d222da...`; runs 2 and 3 produced a 6.24 s artifact with SHA256 beginning `7b160c...`. Additional runs 4 and 5 matched the second hash exactly.

The retained classification is:

```text
FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE
cause: unproven
```

This repository therefore does not claim that every request is universally bitwise deterministic.

## MIX04 post-processing

The accepted MIX04 variant uses seed 12346, temperature 0.65, and loudness normalization. The normalization benchmark is separate from model-generation timing. Its measured mean was approximately 0.316 s across five post-processing runs.

## Raw-results retention

The 313,295-byte raw per-request telemetry file is intentionally omitted from the Git source tree because it expands to 15,339 logical lines. `benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json` records its SHA256, byte size, line accounting, retained authority path, and omission rationale.
