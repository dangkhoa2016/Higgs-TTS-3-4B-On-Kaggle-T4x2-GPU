# Đóng góp

> 🌐 Ngôn ngữ / Language: [English](CONTRIBUTING.md) | **Tiếng Việt**

Cảm ơn bạn đã đóng góp cho dự án kiểm định kỹ thuật độc lập này.

## Phạm vi

Đóng góp nên cải thiện runtime Kaggle T4x2, khả năng tái lập, chất lượng evidence, tài liệu, test hoặc repository governance. Không thêm model weights, bulk audio đã generate, private credentials hoặc vendored upstream repositories.

## Development contract

1. Giữ nguyên historical evidence; không rewrite failure để kết quả trông đẹp hơn.
2. Giữ human-facing documentation song ngữ EN/VI với reciprocal language links.
3. Dùng focused commits và giữ ordinary diff quanh hoặc dưới 600 changed lines.
4. Chạy `make verify` trước khi gửi thay đổi.
5. Benchmark rerun phải dùng output directory mới; không tùy tiện overwrite retained authority.

## Thay đổi runtime

Runtime claim phải được hỗ trợ bằng reproducible evidence. Nếu thay đổi GPU placement, sampling, memory setting hoặc benchmark semantics, cần có focused tests và giải thích quan hệ với accepted baseline.

## Pull requests

Mô tả hardware/runtime đã dùng, exact reproduction steps, affected evidence paths, test đã chạy và known limitations. Không đưa token, credential, private URL hoặc personal voice data vào issue hay pull request.

## Licensing

Khi đóng góp repository-authored material, bạn đồng ý nội dung đó được phân phối theo MIT license của repository. Third-party và upstream materials vẫn tuân theo giấy phép riêng.
