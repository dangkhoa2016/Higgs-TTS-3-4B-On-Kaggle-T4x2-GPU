#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=${ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
ENV_FILE=${HIGGS_ENV_FILE:-$ROOT/production/runtime.env}
[[ -f "$ENV_FILE" ]] && set -a && source "$ENV_FILE" && set +a
VENV=${HIGGS_VENV:-$ROOT/.venv312}
SGLOMNI=${SGLOMNI:-$VENV/bin/sgl-omni}
MODEL=${HIGGS_MODEL_PATH:?HIGGS_MODEL_PATH is required}
HOST=${HIGGS_HOST:-127.0.0.1}; PORT=${HIGGS_PORT:-8000}
[[ -x "$SGLOMNI" ]] || { echo "ERROR: missing executable $SGLOMNI" >&2; exit 2; }
[[ -f "$MODEL/model.safetensors" ]] || { echo "ERROR: model not mounted at $MODEL" >&2; exit 3; }
export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
exec "$SGLOMNI" serve \
  --model-path "$MODEL" \
  --host "$HOST" --port "$PORT" \
  --preprocessing.process tts_frontend \
  --audio_encoder.process tts_frontend --audio_encoder.gpu "${HIGGS_AUX_GPU:-1}" \
  --tts_engine.process pipeline --tts_engine.gpu "${HIGGS_TTS_GPU:-0}" \
  --vocoder.process vocoder --vocoder.gpu "${HIGGS_AUX_GPU:-1}" \
  --tts_engine.engine.dtype "${HIGGS_DTYPE:-float16}" \
  --tts_engine.engine.disable_cuda_graph true \
  --tts_engine.engine.max_running_requests "${HIGGS_MAX_RUNNING_REQUESTS:-1}" \
  --tts_engine.engine.mem_fraction_static "${HIGGS_MEM_FRACTION_STATIC:-0.72}" \
  --tts_engine.engine.sampling_backend "${HIGGS_SAMPLING_BACKEND:-pytorch}" \
  --tts_engine.engine.attention_backend "${HIGGS_ATTENTION_BACKEND:-triton}" \
  --log-level info
