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


def test_root_cause_classification_and_uncertainty_are_exact():
    audit = load("evidence/root-cause-audit-2026-10-09.json")
    conclusion = audit["conclusion"]
    assert conclusion["root_cause_class"] == "zero-shot AR acoustic-generation/bootstrap instability before codec decode"
    assert conclusion["confidence"] == "high for layer localization; exact learned-model internal mechanism remains unproven"


def test_mix04_final_acceptance_and_reference_conditioning_policy():
    mix04 = load("evidence/mix04-final-approved.json")
    review = load("evidence/root-cause-human-review-2026-10-09.json")
    matrix = load("evidence/final-acceptance-matrix-2026-10-09.json")
    assert mix04["status"] == "HUMAN_APPROVED"
    assert mix04["seed"] == 12346
    assert mix04["temperature"] == 0.65
    assert review["overall"]["reference_conditioned"] == "CONTENT_ACCEPTABLE_BUT_ACCENT_NOT_PRODUCTION_READY"
    assert matrix["readiness"]["reference_conditioned_default"] == "REJECTED_FOR_PRODUCTION_WITH_CURRENT_SLT_REFERENCE"
    assert matrix["readiness"]["voice_clone_production_claim"] == "PENDING_HUMAN_ACCEPTANCE"


def test_official_warm_benchmark_authority():
    bench = load("evidence/t4x2-official-benchmark-2026-10-09.json")
    assert bench["requests"] == {"cases": 11, "repetitions": 3, "total": 33, "http200": 33}
    perf = bench["performance"]
    assert perf["latency_mean_s"] == 6.013801341697024
    assert perf["aggregate_rtf"] == 1.0868315677765708
    assert perf["gpu0_peak_used_mib"] == 10951
    assert perf["gpu1_peak_used_mib"] == 4511
    strict = bench["reproducibility"]["strict_3x_bitwise"]
    assert strict["stable_count"] == 10
    assert strict["total_cases"] == 11
    en02 = bench["reproducibility"]["en02"]
    assert en02["classification"] == "FIRST_OBSERVATION_DIVERGENCE_THEN_4X_BITWISE_STABLE"
    assert en02["cause"] == "unproven"


def test_raw_results_are_omitted_but_provenance_is_exact():
    provenance = load("benchmarks/t4x2-official-2026-10-09/RAW-RESULTS-PROVENANCE.json")
    assert provenance["sha256"] == "33be6bb0f6e11aefcaa3ce2d1d1a5d44546e48c43636c32918f4614c2914fae2"
    assert provenance["bytes"] == 313295
    assert provenance["line_count"] == 15339
    assert provenance["newline_count"] == 15338
    assert provenance["ends_with_newline"] is False
    assert provenance["committed_to_git"] is False
    assert not (ROOT / "benchmarks/t4x2-official-2026-10-09/results.json").exists()
