# Tổng quan kỹ thuật

> 🌐 Ngôn ngữ / Language: [English](engineering-overview.md) | **Tiếng Việt**

## Mục tiêu

Kiểm định BosonAI Higgs TTS 3 4B trên phần cứng Tesla T4 của Kaggle bằng original weights được mount từ Kaggle, đồng thời công khai evidence cho cả thành công lẫn thất bại.

## Tiến trình kiểm định

1. Xác định model authority và pin runtime stack.
2. Một GPU T4 load model và tạo TTS FP16 thành công.
3. Kiểm tra transport cho English, Vietnamese, control-token, mixed-language và synthetic-reference.
4. Kiểm tra production headroom cho thấy giới hạn thực của một T4: MIX02 cuối cùng bị CUDA OOM sau khi pipeline đã warm đầy đủ.
5. Stage placement T4x2 chuyển audio encoder và vocoder sang GPU1, còn TTS engine giữ ở GPU0.
6. Mixed suite T4x2 phục hồi case trước đó bị lỗi và thiết lập runtime baseline được chấp nhận.
7. Onset audit định vị hành vi lịch sử của VI02/MIX02/MIX03/MIX04 ở zero-shot autoregressive acoustic generation trước codec decode; exact learned internal mechanism vẫn chủ ý được ghi là chưa chứng minh.
8. Các fixed-seed variant và lựa chọn seed/temperature cuối cho MIX04 được review bằng human listening.
9. Official warm benchmark hoàn tất 33/33 HTTP 200 và trở thành performance authority của repository.

## Phần nào sẵn sàng production

Core zero-shot TTS packaging và T4x2 warm benchmark baseline đã được chấp nhận. English, Vietnamese, code-switching và control examples có variant được human acceptance.

Voice cloning là trường hợp khác: runtime transport hoạt động, nhưng project chưa cấp final perceptual production acceptance cho synthetic-reference clone path. Vì vậy repository không claim production-ready voice cloning.

## Chính sách evidence-first

JSON lịch sử functional, headroom, and T4x2 placement được giữ nguyên. Consolidated final acceptance matrix ghi perceptual decision mới nhất nhưng vẫn bảo tồn các failure trước đó. Điều này ngăn README hoặc release note sau này xóa mất engineering path dẫn tới baseline được chấp nhận.
