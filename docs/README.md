# Documentation

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This directory documents the independently engineered Kaggle T4x2 qualification for BosonAI Higgs TTS 3 4B. It is not an official BosonAI release.

## Start here

- [Architecture](architecture.md) — accepted CPU/GPU stage placement and runtime boundaries.
- [Engineering overview](engineering-overview.md) — why the project moved from one T4 to T4x2.
- [Kaggle setup](kaggle-setup.md) — model mount, runtime environment, launch, readiness, and smoke validation.
- [Benchmark methodology](benchmark-methodology.md) — warm benchmark protocol and measurement boundaries.
- [Benchmark results](benchmark-results.md) — official 2026-10-09 warm baseline.
- [Evidence index](evidence-index.md) — machine-readable authority and negative evidence.
- [Reproducibility](reproducibility.md) — rerunning the accepted baseline safely.
- [Troubleshooting](troubleshooting.md) — FlashInfer, memory, readiness, and output protection.
- [Known limitations](known-limitations.md) — scoped claims and unresolved perceptual/reproducibility caveats.
- [Development history](development-history.md) — evidence-backed engineering chronology.

## Authority

Technical claims in these documents are grounded in the retained files under `evidence/`, `benchmarks/`, `manifests/`, and the production scripts in this repository. Historical phase failures remain visible rather than being rewritten away.

The model weights themselves are not stored in Git; normal Kaggle execution mounts `dangkhoa2016/bosonai-higgs-tts-3-4b` separately.
