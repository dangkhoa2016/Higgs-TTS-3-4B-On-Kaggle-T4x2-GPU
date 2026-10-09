import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def test_single_t4_first_tts_functional_success():
    single_t4 = load("evidence/single-t4-first-tts.json")
    assert single_t4["status"] == "PASS"
    first = single_t4["first_successful_tts"]
    assert first["http_status"] == 200
    assert first["sample_rate_hz"] == 24000
    assert first["channels"] == 1


def test_single_t4_preserves_production_headroom_failure():
    headroom = load("evidence/single-t4-production-headroom.json")
    assert headroom["status"] == "FAIL_PRODUCTION_HEADROOM"
    assert headroom["functional_status"] == "PASS_SINGLE_T4_FUNCTIONAL"
    assert headroom["mixed_probe_2"]["failure"] == "CUDA out of memory"
    assert headroom["mixed_probe_2"]["http_status"] == 500


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


def test_t4x2_stage_placement_and_recovery():
    placement = load("evidence/t4x2-stage-placement-validation.json")
    assert placement["layout"]["gpu0"] == ["tts_engine"]
    assert placement["layout"]["gpu1"] == ["audio_encoder", "vocoder"]
    assert placement["layout"]["cpu"] == ["preprocessing"]
    assert placement["tensor_parallel"] is False
    assert placement["mixed_language_suite"]["count"] == 5
    assert placement["mixed_language_suite"]["pass"] == 5
    assert placement["mixed_language_suite"]["previously_oom_case_recovered"] == "mix02"


def test_historical_perceptual_caveats_are_preserved():
    functional = load("evidence/functional-language-control-validation.json")
    placement = load("evidence/t4x2-stage-placement-validation.json")
    assert "VI02 loses initial Hệ" in functional["perceptual_review_2026_10_08"]["vietnamese_baseline"]
    assert "MIX03 near-silent" in functional["perceptual_review_2026_10_08"]["mixed_language"]
    assert placement["perceptual_review_2026_10_08"]["voice_clone"] == "INTELLIGIBLE_BUT_REFERENCE_TOO_LOW_PITCH"


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


def test_showcase_negative_run_preserves_human_and_waveform_failures():
    evidence = load("evidence/kaggle-showcase-human-review-2026-10-09.json")
    assert evidence["source_notebook_sha256"] == "61b5b14b6eda35b43d3b7dcaccfce4eba4f132f83486f4e0d211165ce0307699"
    assert evidence["machine_transport"] == "PASS_8_OF_8_HTTP200"
    assert evidence["overall_showcase_acceptance"] == "FAIL_HUMAN_AND_AUDIO_ACTIVITY"
    assert evidence["human_review"]["NARR01"]["finding"] == "INITIAL_WORD_OMISSION_AT"
    assert evidence["human_review"]["MIX01"]["finding"] == "ALPHANUMERIC_TOKEN_X2_NOT_VERBALIZED"
    assert evidence["human_review"]["VI01"]["finding"] == "SPEECH_STOPS_AFTER_FIRST_SENTENCE_WITH_LONG_SILENT_TAIL"
    vi01 = evidence["waveform_activity"]["VI01"]
    assert vi01["active_audio_ratio"] < 0.20
    assert vi01["longest_near_silence_s"] >= 25.0
    assert vi01["trailing_near_silence_s"] >= 25.0


def test_latest_showcase_human_review_is_scoped_to_nonofficial_kaggle_account():
    evidence = load("evidence/kaggle-showcase-human-review-nonofficial-account-2026-10-10.json")
    assert evidence["source_notebook"] == "new-setup-kaggle-ssh-v4 (3).ipynb"
    assert evidence["executed_release_commit"] == "62e1b78acb28a015c3cc03d2c3b712cf31377007"
    assert evidence["kaggle_account_scope"]["official_project_owner_account"] is False
    assert evidence["kaggle_account_scope"]["official_account_acceptance"] == "PENDING_RERUN"
    assert evidence["decision"]["perceptual_acceptance"] == "PASS_HUMAN_REVIEWED_NON_OFFICIAL_ACCOUNT_RUN"
    assert evidence["decision"]["official_kaggle_account_acceptance"] == "PENDING_RERUN"
    assert evidence["decision"]["showcase_cases_approved"] == 8
    assert evidence["decision"]["synthetic_reference_voices_approved"] == 4
    assert evidence["decision"]["voice_clone_production_claim"] == "PENDING_HUMAN_ACCEPTANCE"
    assert set(evidence["showcase_cases"]) == {"EN01", "VI01", "MIX01", "ONSET01", "EN02", "VI02", "MIX02", "NARR01"}
    assert set(evidence["synthetic_reference_voices"]) == {"VOICE_A", "VOICE_B", "VOICE_C", "VOICE_D"}
    negative = load("evidence/kaggle-showcase-human-review-2026-10-09.json")
    assert negative["overall_showcase_acceptance"] == "FAIL_HUMAN_AND_AUDIO_ACTIVITY"


def test_official_kaggle_account_execution_and_human_review_are_finalized():
    execution = load("evidence/kaggle-official-account-execution-2026-10-10.json")
    review = load("evidence/kaggle-official-account-human-review-2026-10-10.json")
    matrix = load("evidence/final-acceptance-matrix-2026-10-09.json")
    assert execution["kaggle"]["owner"] == "dangkhoa2016"
    assert execution["kaggle"]["script_version_id"] == 356925390
    assert execution["kaggle"]["official_project_owner_account"] is True
    assert execution["release"]["commit_observed_by_execution"] == "e927fe3dc52fb42213ba3ed71bf61f1ae89f8ade"
    assert execution["machine_acceptance"]["official_account_execution"] == "PASS"
    assert execution["machine_acceptance"]["official_account_machine_acceptance"] == "PASS"
    assert execution["fresh_benchmark_reproduction"]["requests_http200"] == 33
    assert execution["fresh_benchmark_reproduction"]["all_cases_hash_reproducible"] is True
    assert execution["executed_notebook"]["public_download_sha256"] == "b3baadb6e2af30b93f24f38308f4a28644e4d63c68cec09185f80cdcd2fe4c2e"
    assert execution["executed_notebook"]["release_asset_filename"] == "Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B-v1.0.0-Official-Executed-Acceptance.ipynb"
    assert execution["perceptual_acceptance"] == "PASS_HUMAN_REVIEWED"
    assert review["kaggle_script_version_id"] == 356925390
    assert review["decision"]["official_perceptual_acceptance"] == "PASS_HUMAN_REVIEWED"
    assert review["decision"]["voice_clone_production_claim"] == "PENDING_HUMAN_ACCEPTANCE"
    scope = review["reported_scope"]
    assert scope["wav_files_reviewed"] == 47
    assert scope["wav_file_breakdown"] == {
        "production_smoke": 1,
        "synthetic_reference_voices": 4,
        "showcase_cases": 8,
        "official_benchmark_measured": 33,
        "official_benchmark_warmup": 1,
    }
    assert sum(scope["wav_file_breakdown"].values()) == 47
    desc = scope["description"].lower()
    assert "approximately" not in desc
    assert "about" not in desc
    assert "khoảng" not in desc
    assert review["benchmark_observations"]["MIX04"]["classification"] == "ACCEPTED_WITH_KNOWN_LOW_RAW_LOUDNESS"
    assert set(review["benchmark_observations"]["MIX04"]["files"]) == {"mix04-r1.wav", "mix04-r2.wav", "mix04-r3.wav"}
    assert matrix["official_kaggle_account_perceptual_acceptance"] == "PASS_HUMAN_REVIEWED"
    assert matrix["readiness"]["voice_clone_production_claim"] == "PENDING_HUMAN_ACCEPTANCE"
