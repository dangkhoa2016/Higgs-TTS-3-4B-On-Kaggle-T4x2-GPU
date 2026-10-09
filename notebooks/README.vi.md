# Kaggle Production Showcase

> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**

Notebook public chuẩn là [`kaggle-production-showcase.ipynb`](kaggle-production-showcase.ipynb). Đây là **reviewer-facing bilingual guided demo** cho cấu hình Higgs TTS 3 4B đã qualify trên Kaggle NVIDIA Tesla T4 x2.

Notebook được tổ chức theo cùng tinh thần với các production notebook gần đây của nhóm dự án này: mỗi phase chính có phần giải thích Anh/Việt ngắn gọn, output quan sát được, evidence gate tường minh và final machine-readable acceptance record.

## Trước khi chạy

1. Tạo hoặc mở một Kaggle Notebook.
2. Chọn **File → Import Notebook → GitHub**.
3. Chọn `dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B` và `notebooks/kaggle-production-showcase.ipynb`.
4. Chọn accelerator **GPU T4 x2**.
5. Bật **Internet ON** để notebook clone immutable release tag.
6. Dùng **Add Input → Models** và attach:
   - model: `dangkhoa2016/bosonai-higgs-tts-3-4b`
   - variation: `transformers/default`
   - version: `1`
7. Bắt đầu từ fresh session và chọn **Run All**.

Model weights chỉ được đọc từ Kaggle Model đã attach. Notebook không tải model từ Hugging Face, không dùng GGUF và không thực hiện clone giọng người thật.

## Luồng guided demo

Notebook hiện có 44 cells: 24 Markdown cells và 20 code cells. Flow cố ý hướng đến reviewer thay vì tối giản thành một automation script ngắn.

1. **Release + architecture overview** — nêu release, hardware, model input, stage placement và acceptance boundaries.
2. **Immutable release bootstrap** — clone annotated tag `v1.0.0`, kiểm tra tag object type và chứng minh peeled target bằng đúng checked-out commit.
3. **T4 x2 + model preflight** — kiểm tra Kaggle, Python 3.12, `uv`, hai Tesla T4 và Version 1 safetensors mount trước khi cài runtime.
4. **Qualified runtime creation** — tạo Python 3.12 virtual environment từ `production/requirements-runtime-lock.txt`.
5. **Runtime provenance** — in Python, PyTorch/CUDA, SGLang, SGLang-Omni, FlashInfer và GPU memory state.
6. **Real service launch** — chạy production T4x2 helper với FlashInfer cold-JIT linker requirement đã được giữ lại.
7. **Readiness + smoke** — chờ `/health` thật, chạy public readiness script rồi gửi actual WAV smoke request.
8. **Reviewer-facing voice showcase** — tạo bốn synthetic reference voice candidate A–D, preview từng giọng rồi chạy riêng tám listening case dài hơn để mỗi case có giải thích, conditioning metadata, metric và audio player ngay tại chỗ.
9. **Showcase evidence table** — ghi `synthetic-reference-voices.json` và `showcase-suite.json`, hiển thị request/audio metadata của cả tám main case và bổ sung RMS-based activity metrics để fail closed khi có silent-tail dài.
10. **Official warm benchmark rerun** — chạy official benchmark entrypoint của repository trong evidence directory mới.
11. **Final machine-readable acceptance** — ghi `FINAL-ACCEPTANCE.json` và chỉ in `ACCEPTANCE=PASS` sau khi các executable gate PASS.
12. **Optional cleanup + limitations** — mặc định giữ service chạy để review, sau đó ghi rõ notebook chứng minh và không chứng minh điều gì.

## Các listening case cho reviewer

Tám main showcase case không bị giấu trong một batch cell. Mỗi case được chạy và hiển thị độc lập sau bốn synthetic reference voice preview:

| Case | Conditioning | Voice profile | Trọng tâm |
| --- | --- | --- | --- |
| `EN01` | zero-shot | `ZERO_SHOT` | Long English baseline |
| `VI01` | zero-shot | `ZERO_SHOT` | Long Vietnamese baseline |
| `MIX01` | synthetic reference | `VOICE_B` | Code-switch Việt → Anh |
| `ONSET01` | synthetic reference | `VOICE_A` | Giữ onset tiếng Việt |
| `EN02` | synthetic reference | `VOICE_B` | Long English conditioned comparison |
| `VI02` | synthetic reference | `VOICE_C` | Long Vietnamese conditioned comparison |
| `MIX02` | synthetic reference | `VOICE_C` | Code-switch Anh → Việt → Anh |
| `NARR01` | synthetic reference | `VOICE_D` | Long-form bilingual narration |

Mỗi case thực hiện `POST /v1/audio/speech` thật, kiểm tra WAV mono 24 kHz cùng minimum listening duration, ghi conditioning mode, voice profile, latency, duration, RTF và SHA-256, rồi render `IPython.display.Audio` ngay bên dưới case. Các case reference-conditioned dùng contract `references[{audio_path,text}]` của model card với WAV được tạo ngay trong cùng notebook session.

Đây là **sample để con người nghe review**. Việc transport/audio-format gate PASS không thay thế perceptual review và không tự nâng pending voice-clone production claim.

## Evidence output

Khi chạy thành công, evidence được ghi tại:

```text
/kaggle/working/higgs-tts-v1.0.0-acceptance/
```

Các file quan trọng gồm `server.log`, `production-smoke.wav`, bốn synthetic reference WAV, tám showcase WAV, `synthetic-reference-voices.json`, `showcase-suite.json`, `official-benchmark-rerun/summary.json` và `FINAL-ACCEPTANCE.json`.

Final JSON liên kết resolved release commit, tag object type, attached model version, T4x2 stage placement, readiness/smoke results, các showcase case đã chạy, benchmark summary và acceptance boundary đã giữ lại.

## Giới hạn của acceptance

`ACCEPTANCE=PASS` nghĩa là các executable gate về release, hardware, model, runtime, service, smoke, showcase transport và benchmark đã hoàn thành trong session đó. Nó **không** tuyên bố universal T4 compatibility, universal request-level bitwise determinism, exact neural mechanism của onset instability đã được chứng minh hay voice cloning đã production-ready.
