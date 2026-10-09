#!/usr/bin/env bash
set -euo pipefail
ROOT=${ROOT:-/kaggle/working/Higgs-TTS-3-4B-On-Kaggle-T4x2-GPU-rewrite}
ARC=${HIGGS_FLASHINFER_CACHE_ARCHIVE:-$ROOT/evidence/jit-cache/flashinfer-0.6.18-sm75-norm-sampling-2026-10-09.tar.gz}
SUM=${HIGGS_FLASHINFER_CACHE_SHA256:-${ARC%.tar.gz}.sha256}
if [[ ! -f "$ARC" || ! -f "$SUM" ]]; then
  echo 'INFO: optional FlashInfer cache artifact not present; cold JIT may run on first use.'
  exit 0
fi
(cd "$(dirname "$ARC")" && sha256sum -c "$(basename "$SUM")")
if [[ "${1:-}" == "--check" ]]; then
  echo 'PASS: cache checksum only'
  exit 0
fi
DEST=${HIGGS_FLASHINFER_CACHE_DEST:-/root/.cache/sglang/.cache/flashinfer}
mkdir -p "$DEST"
tar -xzf "$ARC" -C "$DEST"
echo 'PASS: FlashInfer cache restored'
