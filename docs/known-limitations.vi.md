# Giới hạn đã biết

> 🌐 Ngôn ngữ / Language: [English](known-limitations.md) | **Tiếng Việt**

## Phạm vi phần cứng đã kiểm định

Accepted baseline là Kaggle NVIDIA Tesla T4 x2 với runtime stack và stage placement đã ghi lại. Repository không chứng minh universal compatibility cho mọi T4 host, CUDA/driver combination hoặc deployment environment khác.

## Single-T4 production headroom

Một T4 có thể chạy functional inference, nhưng qualified single-T4 headroom qualification state fail production headroom. MIX02 bị CUDA OOM sau khi pipeline sử dụng gần hết memory GPU0. Vì vậy single-T4 không phải production-safe baseline mà project claim.

## Zero-shot onset instability

Historical VI02/MIX02 onset loss, MIX03 near-silence và MIX04 onset behavior được định vị với high confidence ở zero-shot autoregressive acoustic generation/bootstrap trước codec decode.

Exact learned-model internal mechanism vẫn unproven. Tài liệu không được biến kết quả localization này thành causal claim mạnh hơn.

## Reference-conditioned diagnostic path

Synthetic SLT reference cải thiện onset stability trong giai đoạn chẩn đoán, nhưng human review phát hiện Vietnamese regional-accent/tone realization không mong muốn. Conditioned path đó chỉ dùng diagnostic và bị reject làm current production default.

## Voice cloning

Voice-clone transport/runtime hoạt động với synthetic references, nhưng final perceptual production acceptance vẫn pending. Repository không claim production-ready voice cloning và không dùng real-person voice cloning cho test.

## Bitwise determinism

Mười trên mười một official benchmark cases byte-identical ngay trong ba repetitions. EN02 diverge ở first observation rồi tạo bốn kết quả byte-identical liên tiếp. Cause unproven, vì vậy không claim universal request-level bitwise determinism.

## Phạm vi warm benchmark

Official performance numbers mô tả warm runtime. FlashInfer cold JIT chủ ý bị loại khỏi timing và có thể làm first-use trên fresh environment lâu hơn đáng kể.

## Heavy artifacts

Model weights, Python virtual environment, benchmark WAVs, raw benchmark telemetry và captured FlashInfer cache tarball đều chủ ý không đưa vào Git. Việc chúng không có trong repo là quyết định packaging, không phải evidence rằng chúng chưa từng tồn tại khi qualification.

## Text coverage và silent-tail trong reviewer showcase

Một fresh reviewer run ngày 2026-10-09 phát hiện thêm ba perceptual/content failure: `NARR01` bỏ từ đầu “At”, `MIX01` không đọc literal technical token `x2`, và zero-shot `VI01` chỉ có speech ở câu đầu rồi gần 26 giây near-silence. Run này được giữ tại `evidence/kaggle-showcase-human-review-2026-10-09.json`. Notebook hiện bổ sung waveform-activity gate cho sustained silence, normalize spoken `T4 x2` thành “hai GPU T4”, và giữ token-coverage/perceptual acceptance phụ thuộc rõ ràng vào human listening.
