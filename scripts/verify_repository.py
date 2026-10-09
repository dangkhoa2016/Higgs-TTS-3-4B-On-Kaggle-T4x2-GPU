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
    ".github/CODEOWNERS", ".github/CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.vi.md",
    ".github/CONTRIBUTING.md", ".github/CONTRIBUTING.vi.md",
    ".github/SECURITY.md", ".github/SECURITY.vi.md",
    ".github/SUPPORT.md", ".github/SUPPORT.vi.md",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/PULL_REQUEST_TEMPLATE.vi.md",
    ".github/dependabot.yml", ".github/workflows/repository-audit.yml",
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


def audit(final: bool) -> list[str]:
    errors = []
    required = set(BASE_REQUIRED)
    if final:
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
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the public repository contract")
    parser.add_argument("--pre-final", action="store_true", help="allow docs/governance files scheduled for later tasks to be absent")
    args = parser.parse_args()
    errors = audit(final=not args.pre_final)
    if errors:
        print("REPOSITORY_AUDIT=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REPOSITORY_AUDIT=PASS")
    print(f"MODE={'pre-final' if args.pre_final else 'final'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
