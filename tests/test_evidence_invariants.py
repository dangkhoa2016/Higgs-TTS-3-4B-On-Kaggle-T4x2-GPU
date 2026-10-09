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


def test_phase6_stage_placement_and_recovery():
    phase6 = load("evidence/phase6-summary.json")
    assert phase6["layout"]["gpu0"] == ["tts_engine"]
    assert phase6["layout"]["gpu1"] == ["audio_encoder", "vocoder"]
    assert phase6["layout"]["cpu"] == ["preprocessing"]
    assert phase6["tensor_parallel"] is False
    assert phase6["mixed_language_suite"]["count"] == 5
    assert phase6["mixed_language_suite"]["pass"] == 5
    assert phase6["mixed_language_suite"]["previously_oom_case_recovered"] == "mix02"


def test_historical_perceptual_caveats_are_preserved():
    phase4 = load("evidence/phase4-summary.json")
    phase6 = load("evidence/phase6-summary.json")
    assert "VI02 loses initial Hệ" in phase4["perceptual_review_2026_10_08"]["vietnamese_baseline"]
    assert "MIX03 near-silent" in phase4["perceptual_review_2026_10_08"]["mixed_language"]
    assert phase6["perceptual_review_2026_10_08"]["voice_clone"] == "INTELLIGIBLE_BUT_REFERENCE_TOO_LOW_PITCH"
