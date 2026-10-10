# Changelog

> 🌐 Ngôn ngữ / Language: [English](CHANGELOG.md) | **Tiếng Việt**

Mọi thay đổi đáng chú ý của repository được ghi tại đây. Public release đầu tiên trên clean history là **v1.0.0**.

## 1.0.0 — 2026-10-09

### Runtime qualification

- Kiểm định original Higgs TTS 3 4B weights được mount từ Kaggle với runtime FP16.
- Giữ nguyên functional single-T4 result và single-T4 production-headroom failure về sau.
- Thiết lập accepted T4x2 stage placement: CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder, tensor parallelism disabled.
- Giữ lại FlashInfer cold-JIT `-lcuda` finding và yêu cầu `LD_LIBRARY_PATH` / `LIBRARY_PATH`.

### Acceptance và evidence

- Giữ historical VI02/MIX02 onset loss, MIX03 near-silence, MIX04 onset/pause behavior và việc reject SLT-conditioned production default.
- Ghi các fixed-seed accepted variants và final human-approved MIX04 settings.
- Giữ voice-clone production acceptance ở trạng thái pending thay vì nâng runtime functionality thành perceptual production claim.

### Benchmark

- Publish accepted warm T4x2 benchmark authority: 33/33 HTTP 200, aggregate RTF khoảng 1.086832, GPU peaks 10,951/4,511 MiB.
- Giữ EN02 first-observation divergence rồi bốn output byte-identical; cause vẫn unproven.
- Thêm benchmark tooling chống overwrite và compact provenance cho raw telemetry được loại khỏi Git.

### Repository engineering

- Rebuild repository từ clean Git root với focused reviewable commits.
- Thêm MIT licensing cho repository-authored material, tài liệu song ngữ EN/VI, governance, repository audits và GitHub Actions CI.
- Thêm Kaggle T4x2 production showcase notebook có thể import trực tiếp, verify annotated-tag provenance, phát nghe multilingual acceptance audio và rerun benchmark.
- Loại model weights, virtual environments, bulk WAV outputs, raw benchmark telemetry, secrets và transient caches khỏi Git.
