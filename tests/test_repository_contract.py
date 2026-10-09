import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_repository.py"


def test_repository_verifier_exists_and_passes_prefinal_tree():
    assert VERIFIER.is_file()
    result = subprocess.run(
        ["python3", str(VERIFIER), "--pre-final"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REPOSITORY_AUDIT=PASS" in result.stdout


def test_current_bilingual_license_notes_are_reciprocal():
    en = (ROOT / "LICENSE-NOTES.md").read_text()
    vi = (ROOT / "LICENSE-NOTES.vi.md").read_text()
    assert "[Tiếng Việt](LICENSE-NOTES.vi.md)" in en
    assert "[English](LICENSE-NOTES.md)" in vi


def test_mit_author_is_exact():
    text = (ROOT / "LICENSE").read_text()
    assert "Copyright (c) 2026 Đăng Khoa <i.am@dangkhoa.dev>" in text


def test_public_tree_contains_no_forbidden_payloads():
    forbidden_suffixes = {".safetensors", ".bin", ".pt", ".pth", ".ckpt", ".gguf", ".wav"}
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".superpowers" in path.parts or "docs/superpowers" in path.as_posix():
            continue
        if path.suffix.lower() in forbidden_suffixes or ".venv312" in path.parts:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []
