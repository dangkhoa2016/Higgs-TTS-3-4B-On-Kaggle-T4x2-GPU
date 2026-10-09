from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "production" / "readiness.sh"
SMOKE = ROOT / "production" / "smoke-request.py"


def test_readiness_uses_local_health_endpoint_and_requires_two_gpus():
    text = READINESS.read_text()
    assert "http://${HIGGS_HOST}:${HIGGS_PORT}/health" in text
    assert "GPU_COUNT" in text
    assert '[[ "$GPU_COUNT" -ge 2 ]]' in text
    assert "status')=='healthy'" in text
    assert "running') is True" in text


def test_smoke_request_validates_http_and_wav_contract():
    text = SMOKE.read_text()
    assert "http://127.0.0.1:8000/v1/audio/speech" in text
    assert "status==200" in text
    assert "sample_rate']==24000" in text
    assert "channels']==1" in text
    assert "duration_s']>0" in text
