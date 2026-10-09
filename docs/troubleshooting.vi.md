# Khắc phục sự cố

> 🌐 Ngôn ngữ / Language: [English](troubleshooting.md) | **Tiếng Việt**

## FlashInfer JIT không tìm thấy `-lcuda`

Triệu chứng đã quan sát: fresh environment lỗi khi link FlashInfer JIT operators vì linker không tìm thấy `-lcuda`.

Dùng:

```bash
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

Sau đó restart qualified server path. Retry vẫn có thể lâu hơn trong lúc cold JIT hoàn tất; official benchmark loại khoảng cold compilation này khỏi timing.

## Single-T4 CUDA OOM sau warmup/reference use

Đây là qualified known failure, không phải installation mystery. single-T4 headroom qualification ghi chỉ còn khoảng 65 MiB free trên GPU0 sau voice-clone use, rồi MIX02 lỗi khi cần thêm allocation.

Không dùng một T4 làm production baseline. Hãy dùng accepted T4x2 stage placement trong `production/serve-t4x2.sh`.

## Readiness fail

`production/readiness.sh` kiểm tra hai GPU, mounted model, service health payload và required pipeline stages. Cần xử lý failure cụ thể được in ra trước khi gửi inference traffic.

Các kiểm tra thường dùng:

```bash
nvidia-smi
ls /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1/model.safetensors
curl -fsS http://127.0.0.1:8000/health
```

## Benchmark từ chối output directory

Đây là hành vi chủ ý. Harness từ chối destination không rỗng nếu chưa explicit overwrite, đồng thời có lớp bảo vệ thứ hai cho retained official authority directory.

Với rerun thông thường, chọn directory mới hoặc dùng `production/run-official-benchmark.sh` mà không truyền output argument.

## Optional FlashInfer cache không tồn tại

Git repository không chứa cache tarball. `production/restore-flashinfer-cache.sh` coi việc thiếu cache là non-fatal và exit thành công sau khi thông báo cold JIT có thể chạy.

## Audio content khác dù dùng fixed seed

Không nên lập tức kết luận corruption. EN02 từng có một first-observation divergence rồi bốn output byte-identical. Trước hết hãy đối chiếu runtime/model authority, giữ lại artifact khác biệt và không claim cause nếu chưa có evidence.

## Voice clone quá trầm hoặc bị regional coloring

Runtime transport PASS không đồng nghĩa clone production-approved. Original KAL synthetic reference được đánh giá quá low/heavy, còn SLT-conditioned diagnostic tạo Vietnamese regional/tone characteristics không mong muốn. Policy hiện tại giữ voice-clone production acceptance ở trạng thái pending.
