import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "benchmark_t4x2_official.py"


def load_harness():
    spec = importlib.util.spec_from_file_location("benchmark_harness", HARNESS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_benchmark_case_contract_and_sampling():
    module = load_harness()
    assert len(module.CASES) == 11
    assert module.REPETITIONS == 3
    by_id = {row[0]: row for row in module.CASES}
    assert by_id["mix04"][2:] == (12346, 0.65)
    for case_id, _text, seed, temp in module.CASES:
        if case_id != "mix04":
            assert (seed, temp) == (12345, 0.8)
    assert module.TOP_K == 50
    assert module.MAX_NEW_TOKENS == 384


def test_output_directory_refuses_existing_nonempty_without_overwrite(tmp_path):
    module = load_harness()
    out = tmp_path / "run"
    out.mkdir()
    (out / "existing.txt").write_text("keep")
    with pytest.raises(SystemExit):
        module.prepare_output_dir(out, allow_overwrite=False, allow_authority_overwrite=False)


def test_canonical_authority_requires_second_explicit_override():
    module = load_harness()
    canonical = ROOT / "benchmarks" / "t4x2-official-2026-10-09"
    with pytest.raises(SystemExit):
        module.prepare_output_dir(canonical, allow_overwrite=True, allow_authority_overwrite=False)


def test_summary_preserves_official_metric_schema():
    module = load_harness()
    rows = [
        {
            "case": "en01", "http_status": 200, "wall_s": 2.0, "duration_s": 1.0,
            "rtf": 2.0, "audio_per_wall": 0.5, "sha256": "a",
            "gpu_peak": {0: {"used_mib": 100}, 1: {"used_mib": 50}},
        },
        {
            "case": "en01", "http_status": 200, "wall_s": 3.0, "duration_s": 2.0,
            "rtf": 1.5, "audio_per_wall": 2.0 / 3.0, "sha256": "a",
            "gpu_peak": {0: {"used_mib": 120}, 1: {"used_mib": 60}},
        },
    ]
    summary = module.summarize(rows)
    overall = summary["overall"]
    assert "latency_p95_s" in overall
    assert "audio_per_wall_mean" in overall
    assert "all_cases_hash_reproducible" in overall
    assert overall["all_cases_hash_reproducible"] is True
    assert overall["aggregate_rtf"] == overall["aggregate_wall_s"] / overall["aggregate_audio_s"]
    case = summary["case_summary"]["en01"]
    assert "latency_min_s" in case and "latency_max_s" in case
    assert "audio_per_wall_mean" in case


def test_incomplete_benchmark_summary_fails_closed():
    module = load_harness()
    incomplete = {
        "status": "PARTIAL", "requests_total": 33, "requests_http200": 32,
        "cases": 11, "repetitions": 3,
    }
    with pytest.raises(SystemExit):
        module.require_complete_benchmark(incomplete)


def test_complete_benchmark_summary_passes_fail_closed_gate():
    module = load_harness()
    complete = {
        "status": "PASS", "requests_total": 33, "requests_http200": 33,
        "cases": 11, "repetitions": 3,
    }
    module.require_complete_benchmark(complete)
