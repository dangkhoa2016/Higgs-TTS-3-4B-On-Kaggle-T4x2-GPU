# Contributing on GitHub

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](CONTRIBUTING.vi.md)

The canonical contribution policy is [../CONTRIBUTING.md](../CONTRIBUTING.md). This file summarizes the GitHub-specific review contract.

## Before opening a pull request

- Run `make verify`.
- Keep changes focused and ordinary commits near or below 600 changed lines.
- Keep EN/VI human-facing documents paired.
- Do not include model weights, generated WAV payloads, secrets, or vendored upstream checkouts.
- Preserve historical evidence and clearly distinguish new measurements from retained authority.

## Pull request evidence

State the Kaggle hardware, runtime versions, reproduction command, affected evidence paths, tests run, and any limitations that remain. If a result differs from retained evidence, attach or describe the new artifact rather than overwriting the old record.

## Review priority

Review favors correctness, provenance, reproducibility, scoped claims, and small auditable diffs over cosmetic completeness.
