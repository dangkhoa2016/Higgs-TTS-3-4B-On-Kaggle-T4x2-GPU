# Kiến trúc

> 🌐 Ngôn ngữ / Language: [English](architecture.md) | **Tiếng Việt**

## Baseline đã được chấp nhận

Baseline production được kiểm định dùng stage placement trên hai GPU NVIDIA Tesla T4 của Kaggle thay vì tensor parallelism.

```text
CPU   -> preprocessing
GPU0  -> tts_engine
GPU1  -> audio_encoder + vocoder
TP    -> disabled
```

Layout này được ghi trong `evidence/t4x2-stage-placement-validation.json` và được triển khai bởi `production/serve-t4x2.sh`.

## Vì sao cần layout này

Inference trên một T4 hoạt động về mặt chức năng, nhưng sau warmup/reference use, VRAM còn lại quá ít cho một số eager codec decode allocation. `evidence/single-t4-production-headroom.json` ghi lại MIX02 bị CUDA OOM trong khi server vẫn healthy.

Việc chuyển audio encoder và vocoder sang GPU1 giúp giảm áp lực bộ nhớ ổn định trên GPU0 trong khi vẫn giữ TTS engine trên GPU0. Sau đó T4x2 stage-placement qualification mixed-language suite đạt 5/5 HTTP 200, bao gồm MIX02 trước đó bị OOM.

## Engine contract

TTS engine đã được kiểm định dùng FP16, tắt CUDA graph, một request đang chạy, `mem_fraction_static=0.72`, PyTorch sampling và Triton attention. Server export:

```bash
LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

Đường dẫn môi trường này cần thiết cho FlashInfer cold-JIT link path đã quan sát để resolve `-lcuda`.

## Ranh giới model

Model được mount riêng từ Kaggle tại `/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1`. Repository không commit model weights, và release path được chấp nhận dùng original weights, không GGUF và không release quantization.

## Phạm vi

Kiến trúc này là baseline Kaggle T4x2 đã được kiểm định. Đây không phải claim về khả năng tương thích phổ quát với mọi hệ thống T4, driver stack hoặc workload shape.
