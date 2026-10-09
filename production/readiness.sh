#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=${ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
source "$ROOT/production/runtime.env"
NSMI=$(command -v nvidia-smi || true); [[ -n "$NSMI" ]] || NSMI=/opt/bin/nvidia-smi
[[ -x "$NSMI" ]] || { echo 'FAIL: nvidia-smi missing'; exit 2; }
GPU_COUNT=$($NSMI --query-gpu=name --format=csv,noheader | wc -l)
[[ "$GPU_COUNT" -ge 2 ]] || { echo "FAIL: need >=2 GPUs, found $GPU_COUNT"; exit 3; }
[[ -f "$HIGGS_MODEL_PATH/model.safetensors" ]] || { echo "FAIL: model missing at $HIGGS_MODEL_PATH"; exit 4; }
HEALTH=$(curl -fsS --max-time 5 "http://${HIGGS_HOST}:${HIGGS_PORT}/health") || { echo 'FAIL: health endpoint'; exit 5; }
python3 - "$HEALTH" <<'PY'
import json,sys
x=json.loads(sys.argv[1])
assert x.get('status')=='healthy' and x.get('running') is True, x
need={'preprocessing','audio_encoder','tts_engine','vocoder'}
assert need.issubset(set(x.get('stages',[]))), x
print('PASS: health', json.dumps(x, separators=(',',':')))
PY
$NSMI --query-gpu=index,name,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits
