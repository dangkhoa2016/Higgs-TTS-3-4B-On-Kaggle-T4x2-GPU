# Kaggle T4x2 Qualification cho Higgs TTS 3 4B

[![Repository Audit](https://github.com/dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B/actions/workflows/repository-audit.yml)
![License: MIT (repository code)](https://img.shields.io/badge/code%20license-MIT-blue.svg)
![Model license: Boson Research & Non-Commercial](https://img.shields.io/badge/model%20license-Boson%20Research%20%26%20Non--Commercial-important.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyTorch FP16](https://img.shields.io/badge/PyTorch-FP16-orange.svg)
![SGLang-Omni](https://img.shields.io/badge/SGLang--Omni-0.1.7-blueviolet.svg)
![NVIDIA Tesla T4 x2](https://img.shields.io/badge/GPU-Tesla%20T4%20x2-76B900.svg)
![Kaggle](https://img.shields.io/badge/platform-Kaggle-20BEFF.svg)
![Original weights](https://img.shields.io/badge/weights-original%20%7C%20no%20quantization-success.svg)
![Human listening](https://img.shields.io/badge/core%20TTS-human%20accepted-success.svg)
![Release state](https://img.shields.io/badge/release-v1.0.0-success.svg)

> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**

Một **independent engineering qualification và reproducibility project** để chạy `bosonai/higgs-tts-3-4b` bằng original weights trên Kaggle NVIDIA Tesla T4 x2 GPU. Repository này **không phải official Boson AI release, product, service hoặc endorsement**.

**Built with Higgs TTS 3 licensed from Boson AI USA, Inc.** Model weights chịu sự điều chỉnh của **Boson Higgs TTS 3 Research and Non-Commercial License**, không phải MIT license của repository này.

Dự án được xây dựng theo hướng evidence-first: kết quả thành công, failure, quyết định human listening, benchmark authority, runtime configuration và tooling tái lập đều được giữ cùng nhau để reviewer có thể kiểm tra lại cùng deployment path thay vì chỉ dựa vào screenshot hoặc claim hiệu năng không có authority.

## Release authority

| Hạng mục | Authority |
| --- | --- |
| Repository release | `v1.0.0` |
| Repository release state | **v1.0.0** |
| Kiểu release | Annotated Git tag + GitHub Release |
| Phần cứng mục tiêu | Kaggle NVIDIA Tesla T4 x2 |
| Model source | `dangkhoa2016/bosonai-higgs-tts-3-4b` |
| Model variation | `transformers/default` |
| Model version | `1` |
| Chính sách weights | Original weights, FP16 runtime, không GGUF, không release quantization |
| Core TTS acceptance | Có retained human-accepted variants cho English, Vietnamese và EN-VI code-switching |
| Voice-clone production claim | `PENDING_HUMAN_ACCEPTANCE` |
| Repository CI | `Repository Audit` phải PASS trên release commit |

- **Repository release state:** v1.0.0

Release `v1.0.0` là public release đầu tiên trên clean history sau repository-audit CI qualification và release-asset verification.

## Repository này chứng minh điều gì

Claim của dự án được cố ý giới hạn: một deployment Higgs TTS 3 4B đã qualification cẩn thận có thể chạy tái lập trên Kaggle T4x2 bằng runtime, stage placement, model mirror, scripts, notebook và evidence được giữ trong repository này.

Dự án **không** claim mọi cấu hình T4 đều production-safe, mọi request đều byte-identical giữa các lần chạy, exact neural mechanism của onset instability đã được chứng minh, hay voice cloning đã đạt perceptual production readiness.

Repository cũng giữ negative evidence. Single-T4 inference chạy được về chức năng, nhưng thất bại ở production-headroom requirement sau warm/reference use. Vì vậy accepted deployment baseline là T4x2 chứ không phải single-T4.

## Current acceptance matrix

| Phạm vi | Trạng thái | Evidence / diễn giải |
| --- | --- | --- |
| Original-weight model load | **PASS** | Kaggle mirror Version 1, không dùng GGUF/quantized release path |
| T4x2 server startup | **PASS** | Accepted stage placement và production scripts |
| Health/readiness contract | **PASS** | `/health`, stage assertions và GPU checks |
| English zero-shot TTS | **ACCEPTED** | Retained human-reviewed variants |
| Vietnamese zero-shot TTS | **ACCEPTED** | Retained human-reviewed variants |
| EN-VI code switching | **ACCEPTED** | Retained human-reviewed variants |
| Official warm benchmark | **ACCEPTED** | 33/33 HTTP 200 |
| Official Kaggle run của project owner (`356925390`) | **HUMAN REVIEWED / ACCEPTED** | Machine acceptance PASS; human listening review của fresh official Output PASS. Các WAV benchmark MIX04 raw được chấp nhận với known low raw loudness |
| Latest human-reviewed showcase (Kaggle account không chính thức) | **HUMAN REVIEWED** | 8/8 transport + activity PASS và human listening đã được duyệt cho run đó |
| Single-T4 production headroom | **FAIL** | Memory exhaustion / MIX02 CUDA OOM được giữ làm negative evidence |
| Current SLT-conditioned reference làm default | **REJECTED** | Diagnostic onset cải thiện nhưng Vietnamese regional/tone characteristics không phù hợp |
| Voice-clone production claim | **PENDING_HUMAN_ACCEPTANCE** | Runtime transport hoạt động với synthetic references; perceptual production acceptance vẫn mở |

Trạng thái hợp nhất dạng machine-readable nằm tại [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json).

## Accepted T4x2 architecture

```text
                         ┌──────────────────────────────┐
                         │           CPU host           │
                         │ preprocessing / HTTP control │
                         └──────────────┬───────────────┘
                                        │
                           ┌────────────┴────────────┐
                           │                         │
                 ┌─────────▼─────────┐     ┌────────▼─────────┐
                 │      GPU 0        │     │      GPU 1       │
                 │    tts_engine     │     │  audio_encoder   │
                 │      FP16         │     │    + vocoder     │
                 └───────────────────┘     └──────────────────┘

Tensor parallelism: disabled
```

Qualified engine contract:

| Setting | Qualified value |
| --- | --- |
| `tts_engine.gpu` | `0` |
| `audio_encoder.gpu` | `1` |
| `vocoder.gpu` | `1` |
| dtype | `float16` |
| CUDA graph | disabled |
| `max_running_requests` | `1` |
| `mem_fraction_static` | `0.72` |
| sampling backend | `pytorch` |
| attention backend | `triton` |
| tensor parallelism | disabled |

Một requirement quan trọng của fresh environment được quan sát trong quá trình qualification:

```bash
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

Thiết lập này cho phép FlashInfer cold-JIT linker path đã quan sát resolve được `-lcuda`.

## Qualified software environment

Authority được qualification với:

| Component | Qualified value |
| --- | --- |
| Python | `3.12.3` |
| PyTorch | `2.13.0+cu130` |
| SGLang | `0.5.20` |
| SGLang-Omni | `0.1.7` |
| FlashInfer | `0.6.18` |
| GPU | NVIDIA Tesla T4 x2 |
| Runtime lock | [`production/requirements-runtime-lock.txt`](production/requirements-runtime-lock.txt) |

Kaggle base image có thể thay đổi theo thời gian. Vì vậy release coi lock file, stage placement, readiness checks và retained evidence là reproducibility contract thay vì giả định các notebook image tương lai luôn giống nhau.

## Model authority và mount contract

Khi chạy bình thường trên Kaggle, repository attach model mirror có sẵn thay vì download weights từ Hugging Face:

```text
Kaggle model: dangkhoa2016/bosonai-higgs-tts-3-4b
Variation:    transformers/default
Version:      1
Mounted path: /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1
```

Model-critical SHA256 authority được giữ tại [`manifests/model-critical.sha256`](manifests/model-critical.sha256), cùng metadata tại [`manifests/model-authority.json`](manifests/model-authority.json).

Model weights chủ ý không được commit vào Git và không được duplicate trong GitHub Release assets.

## Cách review nhanh nhất: Kaggle UI

Community-review path được khuyến nghị là production-showcase notebook:

[`notebooks/kaggle-production-showcase.ipynb`](notebooks/kaggle-production-showcase.ipynb)

### Trước khi Run All

1. Trên Kaggle, import notebook từ GitHub repository này.
2. Chọn **GPU T4 x2**.
3. Bật **Internet** để notebook resolve annotated Git tag.
4. Dùng **Add Input → Models** và attach:
   - `dangkhoa2016/bosonai-higgs-tts-3-4b`
   - variation `transformers/default`
   - Version `1`
5. Run All từ một fresh session.

Notebook được thiết kế như một release acceptance path, không phải cosmetic demo. Nó verify annotated tag `v1.0.0`, kiểm tra hai T4, xác nhận model mount, tạo environment Python 3.12, start service thật, chờ health, chạy smoke validation, generate các acceptance WAV có thể nghe trực tiếp, rerun benchmark và ghi `FINAL-ACCEPTANCE.json`.

Xem [`notebooks/README.vi.md`](notebooks/README.vi.md) để có exact UI workflow và reviewer checklist.

## Manual quick start trên Kaggle

Nếu muốn dùng shell path, clone release và attach cùng model Version 1.

Tạo qualified Python 3.12 environment bằng `uv` và cài runtime lock:

```bash
cd /kaggle/working/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B
uv venv --python /usr/bin/python3.12 --seed .venv312
.venv312/bin/python -m pip install --prefer-binary -r production/requirements-runtime-lock.txt
```

Khởi chạy service:

```bash
export ROOT="$PWD"
export HIGGS_VENV="$PWD/.venv312"
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
bash production/start-background.sh
```

Kiểm tra readiness:

```bash
export ROOT="$PWD"
bash production/readiness.sh
```

Chạy smoke request:

```bash
HIGGS_SMOKE_OUTPUT=outputs/production-smoke.wav \
  .venv312/bin/python production/smoke-request.py
```

Chạy official benchmark harness vào một output directory mới:

```bash
export ROOT="$PWD"
bash production/run-official-benchmark.sh
```

Wrapper bảo vệ retained official benchmark authority khỏi bị overwrite ngoài ý muốn.

## Validation stages

Public repository giữ một qualification path theo stage thay vì chỉ show final success configuration.

| Stage | Mục tiêu | Kết quả |
| --- | --- | --- |
| Runtime/model qualification | Xác nhận original-weight load và inference compatibility | PASS |
| Single-T4 functional validation | Kiểm tra một T4 có generate speech được không | Functional PASS |
| Single-T4 production-headroom qualification | Kiểm tra memory headroom sau warm/reference use | FAIL |
| T4x2 stage-placement qualification | Chuyển auxiliary stages sang GPU1 | PASS |
| Root-cause và perceptual audit | Localize onset failures và human-review variants | Qualified with limitations |
| Warm benchmark | Đo accepted T4x2 runtime tuần tự | PASS, 33/33 |
| Public packaging | Scripts, tests, notebook, bilingual docs, CI, release assets | PASS |

## Official warm benchmark — 2026-10-09

Protocol: 11 cases × 3 repetitions, sequential requests, warm runtime. FlashInfer cold-JIT không được tính vào model-generation timing.

| Metric | Result |
| --- | ---: |
| HTTP success | **33 / 33** |
| Mean latency | **6.013801 s** |
| Median latency | **5.979205 s** |
| p95 latency | **7.094262 s** |
| Mean RTF | **1.087838** |
| Aggregate RTF | **1.086832** |
| Aggregate audio | **182.6 s** |
| Aggregate wall | **198.455444 s** |
| GPU0 peak used | **10,951 MiB** |
| GPU1 peak used | **4,511 MiB** |

Benchmark methodology được mô tả trong [`docs/benchmark-methodology.vi.md`](docs/benchmark-methodology.vi.md), kết quả tại [`docs/benchmark-results.vi.md`](docs/benchmark-results.vi.md) và machine-readable authority tại [`evidence/t4x2-official-benchmark-2026-10-09.json`](evidence/t4x2-official-benchmark-2026-10-09.json).

## Ghi chú về reproducibility và determinism

Mười trên mười một benchmark case byte-identical trong ba repetitions đầu. EN02 diverge ở first observation, sau đó repetitions 2-5 byte-identical.

Retained classification:

```text
FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE
cause: unproven
```

Vì vậy repository **không** claim universal request-level bitwise determinism. Dự án báo cáo đúng reproducibility pattern đã quan sát và giữ extra EN02 evidence thay vì làm mượt kết quả thành một claim mạnh hơn.

## Vì sao dùng T4x2 thay vì một T4

Single-T4 inference chạy được về chức năng. Điều đó chưa đủ để trở thành production baseline.

Trong retained single-T4 headroom qualification path, warm/reference use khiến GPU0 khoảng 14,847 MiB used và chỉ còn khoảng 65 MiB free. Một request MIX02 sau đó bị CUDA OOM trong khi server vẫn healthy. Failure này được giữ trong [`evidence/single-t4-production-headroom.json`](evidence/single-t4-production-headroom.json).

T4x2 layout chuyển `audio_encoder` và `vocoder` sang GPU1, còn `tts_engine` ở GPU0. T4x2 stage-placement qualification sau đó hoàn thành five-case mixed-language suite với **5/5 HTTP 200**, bao gồm MIX02 trước đó bị OOM.

Đó là lý do repository claim qualified **T4x2** baseline và chủ ý không quảng bá single-T4 path là production-safe.

## Onset root-cause audit

Historical zero-shot samples gồm:

- VI02 bị mất từ đầu;
- MIX02 bị mất từ đầu;
- MIX03 gần như silent;
- MIX04 có onset/pause behavior.

Investigation loại trừ tokenizer text loss, delay-pattern off-by-one behavior, codec/HTTP WAV clipping, max-token truncation và request concurrency khỏi retained explanation.

Public classification:

```text
zero-shot AR acoustic-generation/bootstrap instability before codec decode
confidence: high for layer localization; exact learned-model internal mechanism remains unproven
```

Raw-code re-decode và API WAV output có correlation khoảng `0.9999998` hoặc cao hơn trong retained audit, hỗ trợ việc localize vấn đề trước codec decode thay vì post-codec/WAV clipping.

Xem [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json).

## Human-listening decisions

Fixed-seed variants tạo accepted VI02, MIX02 và MIX03 outputs. MIX04 được human approval với:

```text
seed=12346
temperature=0.65
top_k=50
max_new_tokens=384
loudnorm=I=-16:TP=-1.5:LRA=7
```

Final MIX04 authority ghi duration `5.84 s` và SHA256 `5b97e250421eb1869c66570609be3e3094a95bf7c4c774b37aec9a40c8a7e8f9`.

Reference-conditioned SLT output cải thiện onset behavior ở diagnostic, nhưng human review phát hiện Vietnamese regional/tone characteristics không phù hợp. Vì vậy nó chỉ là **diagnostic only** và không phải production default.

Voice-clone runtime transport hoạt động với synthetic references, nhưng final perceptual production acceptance vẫn pending. Qualification project này không sử dụng real-person voice cloning.

## Evidence authority và transparency

Evidence hierarchy được làm rõ:

1. **Machine-readable retained evidence** trong [`evidence/`](evidence/).
2. **Benchmark authority** trong [`benchmarks/t4x2-official-2026-10-09/`](benchmarks/t4x2-official-2026-10-09/).
3. **Model provenance** trong [`manifests/`](manifests/).
4. **Executable reproduction path** trong [`production/`](production/) và [`scripts/`](scripts/).
5. **Kaggle community-review notebook** trong [`notebooks/`](notebooks/).
6. **Bilingual interpretation và boundaries** trong [`docs/`](docs/).

Các điểm bắt đầu nên đọc:

- [`docs/evidence-index.vi.md`](docs/evidence-index.vi.md)
- [`evidence/final-acceptance-matrix-2026-10-09.json`](evidence/final-acceptance-matrix-2026-10-09.json)
- [`evidence/root-cause-audit-2026-10-09.json`](evidence/root-cause-audit-2026-10-09.json)
- [`evidence/root-cause-human-review-2026-10-09.json`](evidence/root-cause-human-review-2026-10-09.json)
- [`benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json`](benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json)

Heavy benchmark WAVs, raw telemetry source 15,339 logical lines, model weights, `.venv312`, transient caches và captured FlashInfer cache archives chủ ý không được lưu trong Git.

## Repository layout

```text
.
├── .github/                  # CI, governance, Dependabot, issue/PR templates
├── benchmarks/               # compact retained benchmark authority
├── docs/                     # bilingual architecture, setup, evidence, limits, history
├── evidence/                 # machine-readable qualification và acceptance records
├── manifests/                # model provenance và critical SHA256 authority
├── notebooks/                # Kaggle production-showcase / acceptance notebook
├── production/               # runtime env, launch, readiness, smoke, benchmark wrappers
├── scripts/                  # repository verifier và benchmark harness
├── tests/                    # repository/runtime/benchmark/evidence contracts
├── CHANGELOG.md              # English release history
├── CHANGELOG.vi.md           # Vietnamese release history
├── CITATION.cff              # citation metadata
├── LICENSE                   # MIT cho repository-authored material
├── README.md                 # English release overview
└── README.vi.md              # Vietnamese release overview
```

## Repository audit và CI

Chạy cùng final repository contract ở local:

```bash
make verify-final
```

GitHub Actions workflow verify repository trên Python 3.12 và không chạy heavyweight model inference trong CI. Workflow dùng current major GitHub Actions dependencies (`actions/checkout@v7` và `actions/setup-python@v7`), còn Dependabot được cấu hình để phát hiện dependency drift trong tương lai.

Audit kiểm repository structure, JSON validity, shell syntax, bilingual documentation contracts, release metadata, notebook invariants, evidence invariants, runtime contracts, benchmark schema và các forbidden large/model payloads.

## Security và privacy boundaries

- Không commit model weights vào repository.
- Kaggle, GitHub hoặc Hugging Face credentials không được xuất hiện trong tracked files.
- Release assets chủ ý loại secrets, virtual environments, bulk WAV collections và model payloads.
- Voice-clone qualification dùng synthetic references; accepted core TTS evidence không yêu cầu real-person voice cloning.
- Hướng dẫn báo cáo security issue nằm trong [`.github/SECURITY.vi.md`](.github/SECURITY.vi.md).

## Known limitations

Các boundary quan trọng nhất:

- single-T4 production headroom không được accepted;
- exact onset neural mechanism vẫn unproven;
- không claim universal byte-level determinism;
- voice-clone production acceptance vẫn pending;
- SLT-conditioned diagnostic reference bị reject làm default production reference;
- performance numbers áp dụng cho retained Kaggle T4x2 qualification path, không áp dụng tự động cho mọi GPU/runtime combination.

Xem [`docs/known-limitations.vi.md`](docs/known-limitations.vi.md) để đọc full list.

## Troubleshooting

Bắt đầu từ [`docs/troubleshooting.vi.md`](docs/troubleshooting.vi.md). Các check có giá trị cao:

1. Xác nhận Kaggle expose hai Tesla T4 GPU.
2. Xác nhận model Version 1 được mount đúng expected path.
3. Xác nhận Python 3.12 được sử dụng thay vì notebook image default nếu default mới hơn.
4. Export cả `LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}` và `LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}` trước GPU/CUDA probe hoặc FlashInfer cold-JIT path đầu tiên.
5. Đọc `production/server.pid` và configured server log nếu health không ready.
6. Không tự động quay lại single-T4 rồi so sánh kết quả như thể vẫn là accepted T4x2 baseline.

## Documentation map

Complete bilingual documentation index nằm tại [`docs/README.vi.md`](docs/README.vi.md), liên kết tới:

- architecture;
- engineering overview;
- Kaggle setup;
- benchmark methodology và results;
- evidence index;
- reproducibility guide;
- troubleshooting;
- known limitations;
- development history.

## Release assets

GitHub release `v1.0.0` cung cấp các reviewer-facing assets gọn nhẹ thay vì duplicate model/evidence payload lớn:

- source archive;
- standalone `kaggle-production-showcase.ipynb`;
- machine-readable release manifest;
- `SHA256SUMS.txt`.

Reviewer nên xem annotated Git tag và repository evidence là release authority, còn asset checksums dùng để verify các file đã download.

## License

Repository-authored code, scripts, tests, configuration và documentation được cấp phép MIT. Xem [`LICENSE`](LICENSE) và [`LICENSE-NOTES.vi.md`](LICENSE-NOTES.vi.md).

Boson Higgs TTS 3 model weights và các Higgs Materials khác chịu sự điều chỉnh của **Boson Higgs TTS 3 Research and Non-Commercial License**. Xem bản Agreement upstream nguyên văn tại [`LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt`](LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt), attribution bắt buộc tại [`NOTICE`](NOTICE), và provenance snapshot tại [`LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md`](LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md).

**Built with Higgs TTS 3 licensed from Boson AI USA, Inc.**

Kaggle platform components, SGLang/SGLang-Omni, PyTorch, FlashInfer và third-party software khác vẫn theo license/notice tương ứng. Repository này không cấp commercial license cho Higgs TTS 3.

## Citation

Citation metadata nằm trong [`CITATION.cff`](CITATION.cff). Khi trích dẫn benchmark hoặc acceptance claim, nên chỉ rõ exact release/tag và retained evidence file tương ứng thay vì chỉ trích README summary.

## Project boundary

Repository này mô tả một Kaggle T4x2 deployment đã được qualification cẩn thận và evidence hỗ trợ cho deployment đó. Mục tiêu là làm review và reproduction dễ hơn, không phải phóng đại model capability.

Nếu fresh-session rerun khác retained authority, hãy giữ conflicting evidence, ghi lại runtime/model/environment differences và điều tra divergence thay vì che giấu hoặc normalize kết quả.
