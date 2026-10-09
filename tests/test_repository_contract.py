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


def test_pre_publication_mode_requires_current_tree_but_defers_future_publication_files():
    result = subprocess.run(
        ["python3", str(VERIFIER), "--pre-publication"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "MODE=pre-publication" in result.stdout


def test_repository_audit_workflow_uses_python312_and_final_verification():
    workflow = ROOT / ".github" / "workflows" / "repository-audit.yml"
    text = workflow.read_text()
    assert "python-version: '3.12'" in text or 'python-version: "3.12"' in text
    assert "make verify-final" in text
    assert "actions/checkout@" in text
    assert "actions/setup-python@" in text


def test_production_shell_helpers_are_executable():
    for path in (ROOT / "production").glob("*.sh"):
        assert path.stat().st_mode & 0o111, f"not executable: {path.name}"


def test_final_readme_contract_is_truthful_and_bilingual():
    en = (ROOT / "README.md").read_text()
    vi = (ROOT / "README.vi.md").read_text()
    required_badges = [
        "Repository Audit", "License: MIT", "Python 3.12", "PyTorch FP16",
        "SGLang-Omni", "NVIDIA Tesla T4 x2", "Kaggle", "Original weights",
        "Human listening", "Release state",
    ]
    for token in required_badges:
        assert token in en
        assert token in vi
    assert "> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)" in en
    assert "> 🌐 Ngôn ngữ / Language: [English](README.md) | **Tiếng Việt**" in vi
    assert "independent engineering qualification and deployment project" in en
    assert "not an official BosonAI release" in en
    assert "pre-v1.0.0" in en and "pre-v1.0.0" in vi
    assert "Release v1.0.0" not in en
    assert "Release v1.0.0" not in vi


def test_final_repository_verifier_passes_complete_tree():
    result = subprocess.run(
        ["python3", str(VERIFIER)], cwd=ROOT, text=True, capture_output=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REPOSITORY_AUDIT=PASS" in result.stdout
    assert "MODE=final" in result.stdout
