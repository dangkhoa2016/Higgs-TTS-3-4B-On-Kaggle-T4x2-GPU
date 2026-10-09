import json
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
    assert "actions/checkout@v7" in text
    assert "actions/setup-python@v7" in text


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
    assert "independent engineering qualification and reproducibility project" in en
    assert "not an official Boson AI release, product, service, or endorsement" in en
    assert "release-v1.0.0" in en and "release-v1.0.0" in vi
    assert "Repository release state:** v1.0.0" in en
    assert "Repository release state:** v1.0.0" in vi
    assert "pre-v1.0.0" not in en
    assert "pre-v1.0.0" not in vi
    assert "notebooks/kaggle-production-showcase.ipynb" in en
    assert "notebooks/kaggle-production-showcase.ipynb" in vi



def test_v1_release_metadata_is_consistent():
    en_changelog = (ROOT / "CHANGELOG.md").read_text()
    vi_changelog = (ROOT / "CHANGELOG.vi.md").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    assert "## 1.0.0 — 2026-10-09" in en_changelog
    assert "## 1.0.0 — 2026-10-09" in vi_changelog
    assert "pre-v1.0.0" not in en_changelog
    assert "pre-v1.0.0" not in vi_changelog
    assert "version: 1.0.0" in citation
    assert "date-released: 2026-10-09" in citation


def test_kaggle_showcase_is_reviewer_facing_bilingual_guided_demo():
    nb_path = ROOT / "notebooks" / "kaggle-production-showcase.ipynb"
    nb = json.loads(nb_path.read_text())
    cells = nb.get("cells", [])
    markdown = ["".join(c.get("source", [])) for c in cells if c.get("cell_type") == "markdown"]
    code = ["".join(c.get("source", [])) for c in cells if c.get("cell_type") == "code"]
    joined_md = "\n".join(markdown)
    joined_code = "\n".join(code)

    assert len(cells) >= 28
    assert len(markdown) >= 14
    assert len(code) >= 12
    for token in [
        "Before you run / Trước khi chạy",
        "Architecture / Kiến trúc",
        "Reviewer-facing voice showcase / Showcase giọng nói cho reviewer",
        "Sample 1 — English",
        "Sample 2 — Vietnamese",
        "Sample 3 — Vietnamese → English code-switch",
        "Sample 4 — Onset-focused Vietnamese",
        "Official warm benchmark reproduction / Tái lập benchmark warm chính thức",
        "Final machine-readable acceptance / Nghiệm thu machine-readable cuối",
        "Reproducibility and limitations / Tái lập và giới hạn",
    ]:
        assert token in joined_md
    assert joined_md.count("### English") >= 6
    assert joined_md.count("### Tiếng Việt") >= 6
    assert "def display_showcase_case" in joined_code
    for case_id in ["EN01", "VI01", "MIX01", "ONSET01"]:
        assert f'display_showcase_case("{case_id}")' in joined_code
    assert "SMALL_ACCEPTANCE_HTTP_SUCCESS" in joined_code
    assert "OFFICIAL_BENCHMARK_RERUN=PASS" in joined_code
    assert "ACCEPTANCE=PASS" in joined_code


def test_kaggle_production_showcase_contract():
    nb_path = ROOT / "notebooks" / "kaggle-production-showcase.ipynb"
    meta_path = ROOT / "notebooks" / "kaggle-production-showcase.kernel-metadata.json"
    guide_path = ROOT / "notebooks" / "README.md"
    assert nb_path.is_file()
    assert meta_path.is_file()
    assert guide_path.is_file()
    nb = json.loads(nb_path.read_text())
    joined = "\n".join("".join(cell.get("source", [])) for cell in nb.get("cells", []))
    assert "v1.0.0" in joined
    assert "describe" in joined and "--exact-match" in joined
    assert "refs/tags/" in joined
    assert "EXPECTED_COMMIT" not in joined
    assert "uv" in joined and "/usr/bin/python3.12" in joined
    assert "dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1" in joined
    assert "FINAL-ACCEPTANCE.json" in joined
    assert "IPython.display" in joined
    meta = json.loads(meta_path.read_text())
    assert meta["machine_shape"] == "NvidiaTeslaT4"
    assert meta["enable_gpu"] is True
    assert meta["enable_internet"] is True
    assert "dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1" in meta["model_sources"]

def test_final_repository_verifier_passes_complete_tree():
    result = subprocess.run(
        ["python3", str(VERIFIER)], cwd=ROOT, text=True, capture_output=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REPOSITORY_AUDIT=PASS" in result.stdout
    assert "MODE=final" in result.stdout


def test_kaggle_showcase_bootstraps_current_kaggle_gpu_runtime():
    import json
    nb = json.loads((ROOT / "notebooks/kaggle-production-showcase.ipynb").read_text())
    code = "\n".join("".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "code")
    assert 'LD_LIBRARY_PATH' in code
    assert 'LIBRARY_PATH' in code
    assert '/usr/local/nvidia/lib64' in code
    assert 'VENV = Path("/tmp/higgs-tts-v1.0.0-venv312")' in code
    assert '--prefer-binary' not in code
    assert 'FLASHINFER_SAMPLING_PREWARM=PASS' in code


def test_kaggle_showcase_has_eight_long_form_cases_and_four_synthetic_reference_voices():
    nb = json.loads((ROOT / "notebooks/kaggle-production-showcase.ipynb").read_text())
    joined = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
    for profile in ["VOICE_A", "VOICE_B", "VOICE_C", "VOICE_D"]:
        assert f'"{profile}"' in joined
    for case_id in ["EN01", "EN02", "VI01", "VI02", "MIX01", "MIX02", "NARR01", "ONSET01"]:
        assert f'display_showcase_case("{case_id}")' in joined
    assert 'SHOWCASE_EXPECTED_CASES = 8' in joined
    assert 'payload["references"] = [{' in joined
    assert '"conditioning_mode"' in joined
    assert '"voice_profile"' in joined
    assert '"max_new_tokens": 1024' in joined
    assert 'SYNTHETIC_REFERENCE_VOICES=4/4' in joined


def test_kaggle_showcase_acceptance_and_benchmark_are_fail_closed():
    nb = json.loads((ROOT / "notebooks/kaggle-production-showcase.ipynb").read_text())
    code = "\n".join("".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "code")
    assert 'benchmark_summary["status"] == "PASS"' in code
    assert 'benchmark_summary["requests_http200"] == 33' in code
    assert 'benchmark_summary["requests_total"] == 33' in code
    assert 'SHOWCASE_EXPECTED_CASES = 8' in code
    assert 'machine_pass =' in code
    assert 'assert machine_pass' in code
    assert '"acceptance": "PASS" if machine_pass else "FAIL"' in code
    assert '"acceptance": "PASS",' not in code


def test_kaggle_showcase_audio_activity_gate_and_spoken_text_normalization():
    nb = json.loads((ROOT / "notebooks/kaggle-production-showcase.ipynb").read_text())
    joined = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
    assert 'AUDIO_ACTIVITY_RMS_THRESHOLD = 0.005' in joined
    assert 'AUDIO_ACTIVITY_MIN_RATIO = 0.55' in joined
    assert 'AUDIO_ACTIVITY_MAX_SILENCE_S = 3.0' in joined
    assert 'active_audio_ratio' in joined
    assert 'longest_near_silence_s' in joined
    assert 'trailing_near_silence_s' in joined
    assert '"Hôm nay chúng ta đang chạy một bài acceptance test có đầy đủ release provenance trên Kaggle với hai GPU T4.' in joined
    assert 'Kaggle T4 x2.' not in joined
    assert '"This story begins at the end of a long engineering session,' in joined
    assert '"At the end of a long engineering session,' not in joined


def test_kaggle_showcase_final_acceptance_separates_machine_audio_and_human_review():
    nb = json.loads((ROOT / "notebooks/kaggle-production-showcase.ipynb").read_text())
    code = "\n".join("".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "code")
    assert 'machine_transport_acceptance' in code
    assert 'audio_activity_acceptance' in code
    assert 'perceptual_acceptance' in code
    assert 'PENDING_HUMAN_REVIEW' in code
    assert 'audio_activity_ok' in code
    assert 'assert machine_pass' in code


def test_public_reviewer_surface_contains_no_internal_phase_taxonomy():
    import re
    public_roots = [ROOT / "README.md", ROOT / "README.vi.md", ROOT / "docs", ROOT / "evidence"]
    offenders = []
    path_re = re.compile(r"phase\d", re.I)
    text_re = re.compile(r"\bphase\s*\d", re.I)
    for root in public_roots:
        paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in paths:
            rel = path.relative_to(ROOT).as_posix()
            if path_re.search(rel):
                offenders.append(f"path:{rel}")
                continue
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                continue
            if text_re.search(content) or path_re.search(content):
                offenders.append(f"content:{rel}")
    assert offenders == []


def test_boson_license_compliance_contract():
    license_path = ROOT / "LICENSES/BOSON-HIGGS-TTS-3-RESEARCH-NON-COMMERCIAL.txt"
    notice_path = ROOT / "NOTICE"
    snapshot_path = ROOT / "LICENSES/BOSON-COMPLIANCE-SNAPSHOT.md"
    assert license_path.is_file()
    assert notice_path.is_file()
    assert snapshot_path.is_file()
    license_text = license_path.read_text(encoding="utf-8")
    notice = notice_path.read_text(encoding="utf-8")
    snapshot = snapshot_path.read_text(encoding="utf-8")
    assert "BOSON HIGGS TTS 3 RESEARCH AND NON-COMMERCIAL LICENSE AGREEMENT" in license_text
    assert "Last Updated: July 8, 2026" in license_text
    assert "Boson Higgs TTS 3 is licensed under the Boson Higgs TTS 3 Research and Non-Commercial License, Copyright (c) Boson AI USA, Inc. All Rights Reserved." in notice
    assert "Built with Higgs TTS 3 licensed from Boson AI USA, Inc." in notice
    assert "0382189330b87c38517530e4e5bf0c9dfeb6c7bfbe62812577ddcb73e09a60c5" in snapshot
    assert "No separate NOTICE file was present" in snapshot
    model_hashes = (ROOT / "manifests/model-critical.sha256").read_text(encoding="utf-8")
    authority = (ROOT / "manifests/model-authority.json").read_text(encoding="utf-8")
    assert "0382189330b87c38517530e4e5bf0c9dfeb6c7bfbe62812577ddcb73e09a60c5  LICENSE" in model_hashes
    assert "b2640a3741dc4035d9eb9e0c26696142a10f8caf208d0d8d6e2600947d6fc8d7  NOTICE" in model_hashes
    assert '"NOTICE"' in authority and '"bytes": 149' in authority
    for rel in ("README.md", "README.vi.md", "LICENSE-NOTES.md", "LICENSE-NOTES.vi.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "Boson Higgs TTS 3 Research and Non-Commercial License" in text
        assert "Built with Higgs TTS 3 licensed from Boson AI USA, Inc." in text


def test_public_software_name_is_not_led_by_higgs_mark():
    expected = "Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B"
    for rel in ("README.md", "README.vi.md", "CITATION.cff"):
        assert expected in (ROOT / rel).read_text(encoding="utf-8")
    title = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
    assert not title.startswith("Higgs TTS 3")
