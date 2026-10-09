# Changelog

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](CHANGELOG.vi.md)

All notable repository changes are documented here. The project is currently **pre-v1.0.0**; no v1.0.0 release is claimed by this file.

## Unreleased — pre-v1.0.0

### Runtime qualification

- Qualified original Higgs TTS 3 4B weights mounted from Kaggle with an FP16 runtime.
- Preserved the functional single-T4 result and the later single-T4 production-headroom failure.
- Established the accepted T4x2 stage placement: CPU preprocessing, GPU0 TTS engine, GPU1 audio encoder + vocoder, tensor parallelism disabled.
- Preserved the FlashInfer cold-JIT `-lcuda` finding and required `LIBRARY_PATH` handling.

### Acceptance and evidence

- Preserved historical VI02/MIX02 onset loss, MIX03 near-silence, MIX04 onset/pause behavior, and the rejected SLT-conditioned production default.
- Recorded fixed-seed accepted variants and final human-approved MIX04 settings.
- Kept voice-clone production acceptance pending rather than promoting runtime functionality to a perceptual production claim.

### Benchmark

- Published the accepted warm T4x2 benchmark authority: 33/33 HTTP 200, aggregate RTF about 1.086832, GPU peaks 10,951/4,511 MiB.
- Preserved the EN02 first-observation divergence followed by four byte-identical outputs; cause remains unproven.
- Added overwrite-safe benchmark tooling and compact provenance for omitted raw telemetry.

### Repository engineering

- Rebuilt the repository from a clean Git root with focused reviewable commits.
- Added MIT licensing for repository-authored material, bilingual EN/VI documentation, governance, repository audits, and GitHub Actions CI.
- Excluded model weights, virtual environments, bulk WAV outputs, raw benchmark telemetry, secrets, and transient caches from Git.
