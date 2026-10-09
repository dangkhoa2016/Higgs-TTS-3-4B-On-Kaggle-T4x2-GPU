# T4x2 Official Warm Benchmark — 2026-10-09

> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**

Thư mục này là benchmark authority nhỏ gọn, có thể review cho accepted Higgs TTS 3 4B Kaggle T4x2 baseline. Đây là evidence, không phải runtime code: các file tại đây giải thích điều kiện chạy, số đo, quan sát về reproducibility và provenance đứng sau những con số performance được repository và release công bố.

Để chạy workflow thực tế, dùng [`../../notebooks/kaggle-production-showcase.ipynb`](../../notebooks/kaggle-production-showcase.ipynb) và benchmark harness tại [`../../scripts/benchmark_t4x2_official.py`](../../scripts/benchmark_t4x2_official.py).

## Benchmark này chứng minh điều gì

Warm benchmark được giữ lại dùng accepted stage placement:

- CPU: preprocessing
- GPU0: `tts_engine`
- GPU1: `audio_encoder + vocoder`
- tensor parallelism: tắt
- requests: chạy tuần tự
- fixed seed cho từng case
- repetitions: 3 cho mỗi case
- cases: 11
- measured requests: 33
- HTTP 200: 33 / 33

FlashInfer cold JIT chủ ý không được tính vào warm timing. Cold-start behavior được document riêng trong repository evidence.

## Frozen baseline results

| Metric | Retained result |
| --- | ---: |
| Mean latency | 6.013801 s |
| Median latency | 5.979205 s |
| p95 latency | 7.094262 s |
| Mean RTF | 1.087838 |
| Aggregate RTF | 1.086832 |
| Aggregate generated audio | 182.6 s |
| Aggregate wall time | 198.455444 s |
| GPU0 peak used | 10,951 MiB |
| GPU1 peak used | 4,511 MiB |

RTF là wall time chia cho generated-audio duration. RTF gần 1 nghĩa là xấp xỉ một giây compute wall time cho mỗi giây audio được sinh trong sequential benchmark profile này.

Các con số này là **frozen official baseline**. Không nên âm thầm thay chúng bằng số từ các lần rerun notebook sau này, vì generated duration, runtime state hoặc chi tiết execution khác có thể thay đổi giữa các run. Một fresh-release acceptance run về sau dùng để xác minh published release path; nó không tự động thay thế benchmark authority này.

## File map

### `benchmark-meta.json`

Mô tả benchmark context trước khi đo: health state, T4x2 placement, GPU memory state, repetition count, telemetry sampling interval và warm/cold policy.

### `summary.json`

Machine-readable benchmark summary chính. File này chứa overall performance, latency/RTF theo từng case, GPU peaks, generated-audio durations và SHA-256 của từng repetition.

### `en02-extra-repro.json`

Giữ lại investigation bổ sung cho EN02. First observation của EN02 khác, trong khi repetitions 2 đến 5 hội tụ về cùng output 6.24 giây và byte-identical. Repository không khẳng định exact cause; cause vẫn là unproven.

### `postprocess-summary.json`

Ghi riêng chi phí MIX04 loudness-normalization post-processing. Post-processing time không được tính vào model-generation latency.

### `RAW-RESULTS-PROVENANCE.json`

Ghi provenance cho raw `results.json` không commit. Raw telemetry gốc có 15,339 logical lines và chủ ý không được đưa vào Git source tree. SHA-256, byte size, authority path và omission reason vẫn được giữ tại đây để public claims còn audit trail rõ ràng.

## Cách hiểu reproducibility

Mười trong mười một case byte-identical ngay trong ba benchmark repetitions đầu. EN02 thì không: first observation khác, còn repetitions 2–5 byte-identical. Vì vậy benchmark này **không** tuyên bố universal bitwise determinism.

Những gì benchmark thực sự hỗ trợ là:

- warm T4x2 runtime thành công cho toàn bộ 33 measured requests;
- sequential latency/RTF ổn định cho retained benchmark profile;
- accepted T4x2 stage-placement memory headroom;
- giữ minh bạch EN02 first-observation anomaly thay vì che giấu.

Xem [`../../evidence/t4x2-official-benchmark-2026-10-09.json`](../../evidence/t4x2-official-benchmark-2026-10-09.json) để đọc compact public verdict và acceptance classification.

## Vì sao raw telemetry và WAV không nằm trong Git

Source repository được chủ ý giữ nhẹ. Bulk per-request telemetry, generated WAV files, model weights, runtime virtual environments và transient caches không phải source artifacts nên không được duplicate vào Git.

Việc omission là minh bạch chứ không âm thầm: `RAW-RESULTS-PROVENANCE.json` giữ checksum và size của raw result, còn các summary/evidence file đã commit giữ những public benchmark claims cần thiết cho review.

## Community reviewer nên dùng thư mục này như thế nào

Dùng snapshot này để trả lời bốn câu hỏi:

1. **Chính xác benchmark đã chạy cái gì?** Đọc `benchmark-meta.json`.
2. **Performance đo được là bao nhiêu?** Đọc `summary.json`.
3. **Có che giấu anomalous observation không?** Xem `en02-extra-repro.json` và per-case hashes.
4. **Raw results bị loại khỏi Git được ghi nhận ở đâu?** Đọc `RAW-RESULTS-PROVENANCE.json`.

Để fresh-check release end-to-end, chạy Kaggle production showcase notebook. Hãy xem evidence mới sinh từ notebook là fresh validation run, còn thư mục này là frozen official benchmark baseline được release documentation sử dụng.
