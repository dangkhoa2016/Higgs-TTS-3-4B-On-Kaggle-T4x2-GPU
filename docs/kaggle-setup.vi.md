# Thiết lập Kaggle

> 🌐 Ngôn ngữ / Language: [English](kaggle-setup.md) | **Tiếng Việt**

## Phần cứng và attach model

Dùng notebook/session Kaggle có hai GPU NVIDIA Tesla T4 và attach Kaggle model mirror hiện có:

```text
dangkhoa2016/bosonai-higgs-tts-3-4b
variation: transformers/default
version: 1
```

Model path dự kiến sau khi mount:

```text
/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

Production execution thông thường không download model từ Hugging Face.

## Runtime environment

Môi trường đã được kiểm định ghi nhận Python 3.12.3, PyTorch 2.13.0+cu130, SGLang 0.5.20, SGLang-Omni 0.1.7 và FlashInfer 0.6.18. `production/requirements-runtime-lock.txt` giữ lại toàn bộ package set đã capture.

Trước khi launch, bảo đảm CUDA driver library path khả dụng:

```bash
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

## Khởi chạy

Từ repository root:

```bash
export ROOT="$PWD"
bash production/serve-t4x2.sh
```

Để chạy background:

```bash
export ROOT="$PWD"
bash production/start-background.sh
```

Layout được chấp nhận là CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder và tensor parallelism bị tắt.

## Readiness và smoke validation

Khi service đang chạy:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

Smoke helper yêu cầu HTTP 200, WAV mono 24 kHz và duration dương. Helper này không mở public tunnel.

## FlashInfer cache

`production/restore-flashinfer-cache.sh` hỗ trợ preserved FlashInfer cache theo kiểu optional khi cache được cung cấp từ bên ngoài. Cache tarball chủ ý không commit vào Git. Nếu cache không tồn tại, helper exit cleanly và môi trường có thể thực hiện cold JIT compilation.

## Chạy lại benchmark

Chỉ chạy benchmark sau khi readiness pass. Wrapper mặc định tạo output directory mới để authority chính thức ngày 2026-10-09 không bị overwrite ngoài ý muốn.
