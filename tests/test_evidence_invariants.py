import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def test_phase3_single_t4_functional_success():
    phase3 = load("evidence/phase3-summary.json")
    assert phase3["status"] == "PASS"
    first = phase3["first_successful_tts"]
    assert first["http_status"] == 200
    assert first["sample_rate_hz"] == 24000
    assert first["channels"] == 1


def test_phase5_preserves_production_headroom_failure():
    phase5 = load("evidence/phase5-summary.json")
    assert phase5["status"] == "FAIL_PRODUCTION_HEADROOM"
    assert phase5["functional_status"] == "PASS_SINGLE_T4_FUNCTIONAL"
    assert phase5["mixed_probe_2"]["failure"] == "CUDA out of memory"
    assert phase5["mixed_probe_2"]["http_status"] == 500


def test_model_authority_and_model_hash_are_exact():
    authority = load("manifests/model-authority.json")
    assert authority["kaggle_model_id"] == "dangkhoa2016/bosonai-higgs-tts-3-4b"
    assert authority["variation"] == "transformers/default"
    assert authority["version"] == "1"
    checksums = (ROOT / "manifests/model-critical.sha256").read_text()
    assert "2f7965264c360b38180885006944aa16bd1de20f4e6cff79f6473bfcf8ae3d5a  model.safetensors" in checksums


def test_production_smoke_authority():
    smoke = load("evidence/production-smoke-2026-10-09.json")
    assert smoke["http_status"] == 200
    assert smoke["sample_rate"] == 24000
    assert smoke["channels"] == 1
    assert smoke["duration_s"] > 0
