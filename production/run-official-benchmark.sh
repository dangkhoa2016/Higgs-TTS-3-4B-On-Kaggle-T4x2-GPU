#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=${ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
OUT=${1:-$ROOT/benchmarks/t4x2-rerun-$(date -u +%Y%m%dT%H%M%SZ)}
"$ROOT/production/readiness.sh"
exec python3 "$ROOT/scripts/benchmark_t4x2_official.py" --output-dir "$OUT"
