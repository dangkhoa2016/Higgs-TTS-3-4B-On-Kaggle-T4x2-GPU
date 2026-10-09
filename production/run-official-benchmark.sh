#!/usr/bin/env bash
set -euo pipefail
ROOT=${ROOT:-/kaggle/working/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU-rewrite}
OUT=${1:-$ROOT/benchmarks/t4x2-rerun-$(date -u +%Y%m%dT%H%M%SZ)}
"$ROOT/production/readiness.sh"
exec python3 "$ROOT/scripts/benchmark_t4x2_official.py" --output-dir "$OUT"
