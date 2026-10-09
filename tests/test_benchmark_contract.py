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
