#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=${ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
ENV_FILE=${HIGGS_ENV_FILE:-$ROOT/production/runtime.env}
[[ -f "$ENV_FILE" ]] && set -a && source "$ENV_FILE" && set +a
PIDFILE=${HIGGS_PID_FILE:-$ROOT/production/server.pid}
LOG=${HIGGS_LOG_FILE:-${HIGGS_SERVER_LOG:-$ROOT/logs/production-t4x2-server.log}}
PORT=${HIGGS_PORT:-8000}
mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOG")"
if curl -fsS --max-time 2 "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
  echo "Server already healthy on port ${PORT}"
  exit 0
fi
nohup "$ROOT/production/serve-t4x2.sh" >"$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "Started PID $(cat "$PIDFILE"); log=$LOG"
