from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / "production" / "runtime.env"
SERVE = ROOT / "production" / "serve-t4x2.sh"


def test_runtime_env_matches_accepted_t4x2_baseline():
    text = ENV.read_text()
    assert "HIGGS_MODEL_PATH=${HIGGS_MODEL_PATH:-/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1}" in text
    assert "HIGGS_TTS_GPU=${HIGGS_TTS_GPU:-0}" in text
    assert "HIGGS_AUX_GPU=${HIGGS_AUX_GPU:-1}" in text
    assert "HIGGS_MEM_FRACTION_STATIC=${HIGGS_MEM_FRACTION_STATIC:-0.72}" in text
    assert "HIGGS_DTYPE=${HIGGS_DTYPE:-float16}" in text
    assert "HIGGS_MAX_RUNNING_REQUESTS=${HIGGS_MAX_RUNNING_REQUESTS:-1}" in text
    assert "HIGGS_SAMPLING_BACKEND=${HIGGS_SAMPLING_BACKEND:-pytorch}" in text
    assert "HIGGS_ATTENTION_BACKEND=${HIGGS_ATTENTION_BACKEND:-triton}" in text


def test_serve_script_pins_stage_placement_and_engine_contract():
    text = SERVE.read_text()
    required = [
        '--audio_encoder.gpu "${HIGGS_AUX_GPU:-1}"',
        '--tts_engine.gpu "${HIGGS_TTS_GPU:-0}"',
        '--vocoder.gpu "${HIGGS_AUX_GPU:-1}"',
        '--tts_engine.engine.dtype "${HIGGS_DTYPE:-float16}"',
        '--tts_engine.engine.disable_cuda_graph true',
        '--tts_engine.engine.max_running_requests "${HIGGS_MAX_RUNNING_REQUESTS:-1}"',
        '--tts_engine.engine.mem_fraction_static "${HIGGS_MEM_FRACTION_STATIC:-0.72}"',
        '--tts_engine.engine.sampling_backend "${HIGGS_SAMPLING_BACKEND:-pytorch}"',
        '--tts_engine.engine.attention_backend "${HIGGS_ATTENTION_BACKEND:-triton}"',
    ]
    for needle in required:
        assert needle in text
    assert "tensor_parallel" not in text.lower()
    assert "export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}" in text

START = ROOT / "production" / "start-background.sh"
RESTORE = ROOT / "production" / "restore-flashinfer-cache.sh"


def test_start_helper_uses_canonical_serve_and_safe_runtime_paths():
    text = START.read_text()
    assert "serve-t4x2.sh" in text
    assert "HIGGS_PID_FILE" in text
    assert "HIGGS_LOG_FILE" in text
    assert "nohup" in text


def test_cache_restore_is_optional_when_archive_is_missing():
    text = RESTORE.read_text()
    assert "HIGGS_FLASHINFER_CACHE_ARCHIVE" in text
    assert "optional" in text.lower()
    assert "exit 0" in text


def test_public_shell_helpers_derive_repository_root_instead_of_private_working_paths():
    private_roots = [
        "/kaggle/working/higgs-tts-3-t4x2",
        "/kaggle/working/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU-rewrite",
    ]
    for path in (ROOT / "production").glob("*.sh"):
        text = path.read_text()
        for private_root in private_roots:
            assert private_root not in text, f"private ROOT leaked in {path.name}"
        assert "BASH_SOURCE[0]" in text, f"repository root not derived in {path.name}"


def test_runtime_env_preserves_caller_overrides():
    text = ENV.read_text()
    assert "HIGGS_MODEL_PATH=${HIGGS_MODEL_PATH:-/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1}" in text
    assert "HIGGS_PORT=${HIGGS_PORT:-8000}" in text
    assert "HIGGS_TTS_GPU=${HIGGS_TTS_GPU:-0}" in text


def test_background_helper_loads_runtime_env_before_health_probe():
    text = START.read_text()
    source_pos = text.index('source "$ENV_FILE"')
    port_pos = text.index('PORT=${HIGGS_PORT:-8000}')
    assert source_pos < port_pos
