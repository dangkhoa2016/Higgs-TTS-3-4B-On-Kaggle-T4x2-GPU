#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".safetensors", ".bin", ".pt", ".pth", ".ckpt", ".gguf", ".wav"}
BASE_REQUIRED = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "LICENSE-NOTES.md",
    "LICENSE-NOTES.vi.md",
    "CITATION.cff",
    "production/runtime.env",
    "production/serve-t4x2.sh",
    "production/start-background.sh",
    "production/restore-flashinfer-cache.sh",
    "production/readiness.sh",
    "production/smoke-request.py",
}
FINAL_REQUIRED = {
    "README.md", "README.vi.md", "CHANGELOG.md", "CHANGELOG.vi.md",
    "CONTRIBUTING.md", "CONTRIBUTING.vi.md", "Makefile",
    "docs/README.md", "docs/README.vi.md",
    "docs/architecture.md", "docs/architecture.vi.md",
    "docs/engineering-overview.md", "docs/engineering-overview.vi.md",
    "docs/kaggle-setup.md", "docs/kaggle-setup.vi.md",
    "docs/benchmark-methodology.md", "docs/benchmark-methodology.vi.md",
    "docs/benchmark-results.md", "docs/benchmark-results.vi.md",
    "docs/evidence-index.md", "docs/evidence-index.vi.md",
    "docs/reproducibility.md", "docs/reproducibility.vi.md",
    "docs/troubleshooting.md", "docs/troubleshooting.vi.md",
    "docs/known-limitations.md", "docs/known-limitations.vi.md",
    "docs/development-history.md", "docs/development-history.vi.md",
    "notebooks/README.md", "notebooks/README.vi.md",
    "notebooks/kaggle-production-showcase.ipynb",
    "notebooks/kaggle-production-showcase.kernel-metadata.json",
    ".github/CODEOWNERS", ".github/CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.vi.md",
    ".github/CONTRIBUTING.md", ".github/CONTRIBUTING.vi.md",
    ".github/SECURITY.md", ".github/SECURITY.vi.md",
    ".github/SUPPORT.md", ".github/SUPPORT.vi.md",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/PULL_REQUEST_TEMPLATE.vi.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md", ".github/ISSUE_TEMPLATE/bug_report.vi.md",
    ".github/ISSUE_TEMPLATE/feature_request.md", ".github/ISSUE_TEMPLATE/feature_request.vi.md",
    ".github/ISSUE_TEMPLATE/documentation.md", ".github/ISSUE_TEMPLATE/documentation.vi.md",
    ".github/ISSUE_TEMPLATE/question.md", ".github/ISSUE_TEMPLATE/question.vi.md",
    ".github/dependabot.yml", ".github/workflows/repository-audit.yml",
    "NOTICE",
    "LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt",
    "LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md",
}
PUBLICATION_FUTURE = {
    "README.md", "README.vi.md",
    "CHANGELOG.md", "CHANGELOG.vi.md",
    "docs/development-history.md", "docs/development-history.vi.md",
    "notebooks/README.md", "notebooks/README.vi.md",
    "notebooks/kaggle-production-showcase.ipynb",
    "notebooks/kaggle-production-showcase.kernel-metadata.json",
}


def public_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if ".git" in parts or ".superpowers" in parts or rel.as_posix().startswith("docs/superpowers/"):
            continue
        yield rel, path


def paired_markdown_errors():
    errors = []
    pairs = []
    for rel, path in public_files():
        if path.suffix != ".md" or rel.name.endswith(".vi.md"):
            continue
        vi = rel.with_name(rel.stem + ".vi.md")
        if (ROOT / vi).exists():
            pairs.append((rel, vi))
    for en, vi in pairs:
        en_text = (ROOT / en).read_text(encoding="utf-8")
        vi_text = (ROOT / vi).read_text(encoding="utf-8")
        en_target = vi.name
        vi_target = en.name
        if en_target not in en_text:
            errors.append(f"missing VI language switch in {en}")
        if vi_target not in vi_text:
            errors.append(f"missing EN language switch in {vi}")
    return errors


def readme_errors():
    errors = []
    en_path = ROOT / "README.md"
    vi_path = ROOT / "README.vi.md"
    if not en_path.exists() or not vi_path.exists():
        return errors
    en = en_path.read_text(encoding="utf-8")
    vi = vi_path.read_text(encoding="utf-8")
    badge_tokens = [
        "Repository Audit", "License: MIT", "Python 3.12", "PyTorch FP16",
        "SGLang-Omni", "NVIDIA Tesla T4 x2", "Kaggle", "Original weights",
        "Human listening", "Release state",
    ]
    for token in badge_tokens:
        if token not in en or token not in vi:
            errors.append(f"README badge/header token missing: {token}")
    if "> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)" not in en:
        errors.append("README.md language switch mismatch")
    if "> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**" not in vi:
        errors.append("README.vi.md language switch mismatch")
    if "independent engineering qualification and reproducibility project" not in en:
        errors.append("README independent-project disclaimer missing")
    if "not an official Boson AI release, product, service, or endorsement" not in en:
        errors.append("README upstream-official disclaimer missing")
    if "release-v1.0.0" not in en or "release-v1.0.0" not in vi:
        errors.append("README v1.0.0 release badge missing")
    if "Repository release state:** v1.0.0" not in en or "Repository release state:** v1.0.0" not in vi:
        errors.append("README v1.0.0 release state missing")
    if "pre-v1.0.0" in en or "pre-v1.0.0" in vi:
        errors.append("README still contains pre-release state")
    return errors



def kaggle_notebook_errors():
    errors = []
    nb_path = ROOT / "notebooks/kaggle-production-showcase.ipynb"
    meta_path = ROOT / "notebooks/kaggle-production-showcase.kernel-metadata.json"
    if not nb_path.is_file() or not meta_path.is_file():
        return errors
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid Kaggle notebook JSON: {exc}"]
    joined = "\n".join("".join(cell.get("source", [])) for cell in nb.get("cells", []))
    required = ["v1.0.0", "--exact-match", "refs/tags/", "/usr/bin/python3.12",
                "FINAL-ACCEPTANCE.json", "IPython.display"]
    for token in required:
        if token not in joined:
            errors.append(f"Kaggle notebook contract token missing: {token}")
    if "EXPECTED_COMMIT" in joined:
        errors.append("Kaggle notebook contains impossible self-referential commit pin")
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid Kaggle kernel metadata JSON: {exc}")
        return errors
    if meta.get("machine_shape") != "NvidiaTeslaT4" or meta.get("enable_gpu") is not True:
        errors.append("Kaggle kernel metadata does not require NvidiaTeslaT4 GPU")
    model = "dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1"
    if model not in meta.get("model_sources", []):
        errors.append("Kaggle kernel metadata model Version 1 source missing")
    return errors

def audit(mode: str) -> list[str]:
    errors = []
    required = set(BASE_REQUIRED)
    if mode == "pre-publication":
        required |= FINAL_REQUIRED - PUBLICATION_FUTURE
    elif mode == "final":
        required |= FINAL_REQUIRED
    for rel in sorted(required):
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")
    for rel, path in public_files():
        if ".venv312" in rel.parts:
            errors.append(f"forbidden virtualenv path: {rel}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden payload: {rel}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"invalid JSON {rel}: {exc}")
    license_path = ROOT / "LICENSE"
    if license_path.exists() and "Copyright (c) 2026 Đăng Khoa <i.am@dangkhoa.dev>" not in license_path.read_text(encoding="utf-8"):
        errors.append("MIT author line mismatch")
    errors.extend(paired_markdown_errors())
    if mode == "final":
        errors.extend(readme_errors())
        errors.extend(kaggle_notebook_errors())
        changelog_en = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        changelog_vi = (ROOT / "CHANGELOG.vi.md").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        if "## 1.0.0 — 2026-10-09" not in changelog_en or "## 1.0.0 — 2026-10-09" not in changelog_vi:
            errors.append("v1.0.0 changelog entry missing")
        if "pre-v1.0.0" in changelog_en or "pre-v1.0.0" in changelog_vi:
            errors.append("changelog still contains pre-release state")
        history_en = (ROOT / "docs/development-history.md").read_text(encoding="utf-8")
        history_vi = (ROOT / "docs/development-history.vi.md").read_text(encoding="utf-8")
        if "pre-v1.0.0" in history_en or "pre-v1.0.0" in history_vi:
            errors.append("development history still contains stale pre-release boundary")
        if "version: 1.0.0" not in citation or "date-released: 2026-10-09" not in citation:
            errors.append("CITATION.cff v1.0.0 metadata missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the public repository contract")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pre-final", action="store_true", help="legacy build mode: require only the base runtime/legal tree")
    group.add_argument("--pre-publication", action="store_true", help="require the complete Task 1-16 tree while deferring only Task 17-18 publication files")
    args = parser.parse_args()
    mode = "pre-final" if args.pre_final else "pre-publication" if args.pre_publication else "final"
    errors = audit(mode=mode)
    if errors:
        print("REPOSITORY_AUDIT=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REPOSITORY_AUDIT=PASS")
    print(f"MODE={mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
