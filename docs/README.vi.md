# Tài liệu

> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**

Thư mục này mô tả quá trình kiểm định kỹ thuật độc lập Higgs TTS 3 4B trên Kaggle T4x2. Đây không phải bản phát hành chính thức của BosonAI.

## Bắt đầu từ đây

- [Kiến trúc](architecture.vi.md) — cách phân bố stage CPU/GPU đã được chấp nhận và các ranh giới runtime.
- [Tổng quan kỹ thuật](engineering-overview.vi.md) — lý do dự án chuyển từ một T4 sang T4x2.
- [Thiết lập Kaggle](kaggle-setup.vi.md) — mount model, môi trường runtime, khởi chạy, readiness và smoke validation.
- [Phương pháp benchmark](benchmark-methodology.vi.md) — protocol warm benchmark và phạm vi đo.
- [Kết quả benchmark](benchmark-results.vi.md) — baseline warm chính thức ngày 2026-10-09.
- [Chỉ mục evidence](evidence-index.vi.md) — authority machine-readable và negative evidence.
- [Khả năng tái lập](reproducibility.vi.md) — cách chạy lại baseline an toàn.
- [Khắc phục sự cố](troubleshooting.vi.md) — FlashInfer, memory, readiness và bảo vệ output.
- [Giới hạn đã biết](known-limitations.vi.md) — phạm vi claim và các caveat còn tồn tại.
- [Lịch sử phát triển](development-history.vi.md) — chronology kỹ thuật dựa trên evidence.
- [Kaggle production showcase](../notebooks/README.vi.md) — import trực tiếp từ GitHub vào Kaggle UI và fresh-session acceptance workflow.

## Authority

Các claim kỹ thuật trong tài liệu được neo vào những file giữ lại trong `evidence/`, `benchmarks/`, `manifests/` và các production script của repository. Những failure lịch sử vẫn được giữ nguyên thay vì bị viết lại cho đẹp hơn.

Model weights không được lưu trong Git; khi chạy trên Kaggle, model `dangkhoa2016/bosonai-higgs-tts-3-4b` được mount riêng.
