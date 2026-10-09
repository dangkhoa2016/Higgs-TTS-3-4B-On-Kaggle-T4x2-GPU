# Đóng góp trên GitHub

> 🌐 Ngôn ngữ / Language: [English](CONTRIBUTING.md) | **Tiếng Việt**

Contribution policy chính nằm tại [../CONTRIBUTING.vi.md](../CONTRIBUTING.vi.md). File này tóm tắt GitHub-specific review contract.

## Trước khi mở pull request

- Chạy `make verify`.
- Giữ thay đổi focused và ordinary commit quanh hoặc dưới 600 changed lines.
- Giữ human-facing documents theo cặp EN/VI.
- Không thêm model weights, generated WAV payloads, secrets hoặc vendored upstream checkouts.
- Giữ nguyên historical evidence và phân biệt rõ measurement mới với retained authority.

## Pull request evidence

Nêu Kaggle hardware, runtime versions, reproduction command, affected evidence paths, test đã chạy và các limitation còn lại. Nếu kết quả khác retained evidence, hãy attach hoặc mô tả artifact mới thay vì overwrite record cũ.

## Ưu tiên review

Review ưu tiên correctness, provenance, reproducibility, scoped claims và small auditable diffs hơn cosmetic completeness.
