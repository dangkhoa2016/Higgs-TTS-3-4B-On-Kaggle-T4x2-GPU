from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / "production" / "runtime.env"
SERVE = ROOT / "production" / "serve-t4x2.sh"


def test_runtime_env_matches_accepted_t4x2_baseline():
    text = ENV.read_text()
    assert "HIGGS_MODEL_PATH=/kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1" in text
    assert "HIGGS_TTS_GPU=0" in text
    assert "HIGGS_AUX_GPU=1" in text
    assert "HIGGS_MEM_FRACTION_STATIC=0.72" in text
    assert "HIGGS_DTYPE=float16" in text
    assert "HIGGS_MAX_RUNNING_REQUESTS=1" in text
    assert "HIGGS_SAMPLING_BACKEND=pytorch" in text
    assert "HIGGS_ATTENTION_BACKEND=triton" in text


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
