# Contributing

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](CONTRIBUTING.vi.md)

Thank you for contributing to this independent engineering qualification project.

## Scope

Contributions should improve the Kaggle T4x2 runtime, reproducibility, evidence quality, documentation, tests, or repository governance. Do not add model weights, generated bulk audio, private credentials, or vendored upstream repositories.

## Development contract

1. Preserve historical evidence; do not rewrite failures to make results look cleaner.
2. Keep human-facing documentation bilingual EN/VI with reciprocal language links.
3. Use focused commits and keep ordinary diffs around or below 600 changed lines.
4. Run `make verify` before submitting changes.
5. Keep benchmark reruns in fresh output directories; never overwrite retained authority casually.

## Runtime changes

Runtime claims must be supported by reproducible evidence. If a change alters GPU placement, sampling, memory settings, or benchmark semantics, include focused tests and explain how it relates to the accepted baseline.

## Pull requests

Describe the hardware/runtime used, exact reproduction steps, affected evidence paths, tests run, and known limitations. Never paste tokens, credentials, private URLs, or personal voice data into issues or pull requests.

## Licensing

By contributing repository-authored material, you agree that it is distributed under the repository MIT license. Third-party and upstream materials remain under their own licenses.
