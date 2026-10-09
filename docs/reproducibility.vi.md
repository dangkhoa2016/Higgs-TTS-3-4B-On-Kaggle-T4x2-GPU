# Khả năng tái lập

> 🌐 Ngôn ngữ / Language: [English](reproducibility.md) | **Tiếng Việt**

## Tái lập môi trường đã kiểm định

Attach Kaggle model `dangkhoa2016/bosonai-higgs-tts-3-4b`, variation `transformers/default`, version `1` và dùng session T4x2. Model path dự kiến cùng toàn bộ Python package set đã capture được ghi trong `production/runtime.env` và `production/requirements-runtime-lock.txt`.

Hãy verify critical model checksums bằng `manifests/model-critical.sha256` trước khi so sánh kết quả giữa các máy.

## Launch accepted baseline

```bash
export ROOT="$PWD"
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/serve-t4x2.sh
```

Ở shell khác, chạy:

```bash
export ROOT="$PWD"
bash production/readiness.sh
python3 production/smoke-request.py
```

Placement được chấp nhận là CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder và tensor parallelism disabled.

## Chạy lại benchmark an toàn

Không target retained directory `benchmarks/t4x2-official-2026-10-09/`. Wrapper tự tạo destination mới có timestamp khi không truyền path:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

Có thể truyền một custom fresh directory làm argument đầu tiên.

## Phần nào nên tái lập được

Official authority chứng minh 33/33 HTTP 200 và latency/RTF ổn định cho qualified warm baseline. Mười trên mười một case byte-identical trong ba repetitions đầu.

Fixed seeds và pinned runtime giúp việc đối chiếu mạnh hơn, nhưng không chứng minh universal byte determinism. EN02 có first observation khác, sau đó repetitions 2-5 ổn định thành một kết quả byte-identical. Cause được ghi rõ là unproven.

## Warm và cold behavior

Official benchmark loại FlashInfer cold JIT khỏi timing. Fresh machine có thể compile FlashInfer operators trước khi đạt warm behavior. Lỗi link `-lcuda` đã quan sát được xử lý bằng `LD_LIBRARY_PATH` cùng `LIBRARY_PATH`; external cache optional có thể tăng tốc migration nhưng không thuộc Git source release.

## Perceptual reproducibility

Repository ghi các human-approved variant cho core TTS cases, nhưng audio quality vẫn là thuộc tính perceptual chứ không phải checksum-only claim. Voice-clone runtime functionality không được hiểu là final production perceptual acceptance.
