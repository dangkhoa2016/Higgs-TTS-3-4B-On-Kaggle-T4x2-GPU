# Chính sách bảo mật

> 🌐 Ngôn ngữ / Language: [English](SECURITY.md) | **Tiếng Việt**

## Phạm vi được hỗ trợ

Security report nên liên quan đến repository-authored scripts, workflows, packaging hoặc documentation trên default branch hiện tại. Vulnerability thuộc upstream model/runtime cũng nên được báo cho upstream project phù hợp khi cần.

## Báo cáo vulnerability

Không đăng exploitable details, credential, token, private URL hoặc sensitive user data trong public issue. Hãy dùng cơ chế private security reporting của GitHub khi khả dụng, hoặc liên hệ repository owner qua contact information đã công khai trong repository metadata.

Cung cấp affected path/version, reproduction steps, impact và safe proof-of-concept details cần thiết để hiểu vấn đề.

## Kỳ vọng phản hồi

Report được review theo best-effort. Project không cam kết response/remediation SLA cố định.

## Secrets

Repository không yêu cầu commit credential. Nếu token vô tình bị lộ, hãy revoke hoặc rotate ngay và loại bỏ nó khỏi toàn bộ reachable history trước khi publish.
