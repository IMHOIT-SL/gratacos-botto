#!/usr/bin/env bash
# AMR Research Dashboard — local API launcher.
# Activates the venv and runs the Dash app on port 8082.
# Stop with Ctrl+C.

set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8082}"

cd "$PROJECT_ROOT"

# --- Sanity checks -----------------------------------------------------------
if [[ ! -d venv ]]; then
    echo "ERROR: venv/ not found at $PROJECT_ROOT/venv"
    echo "  Create it with: python3.12 -m venv venv && venv/bin/pip install -r requirements.txt"
    exit 1
fi

if [[ ! -f dashboard/app.py ]]; then
    echo "ERROR: dashboard/app.py not found"
    exit 1
fi

if ss -tlnp 2>/dev/null | grep -q ":${PORT}\b"; then
    echo "ERROR: Port ${PORT} is already in use:"
    ss -tlnp 2>/dev/null | grep ":${PORT}\b"
    echo "  Stop the offending process or set PORT=<other> before running."
    exit 1
fi

# --- Banner ------------------------------------------------------------------
cat <<EOF
─────────────────────────────────────────────────
  AMR Research Dashboard — local API
  Project:  $PROJECT_ROOT
  Serving:  http://localhost:${PORT}
  Public:   https://resistome.imhoit.com  (run-web.sh required)
  Stop:     Ctrl+C
─────────────────────────────────────────────────
EOF

# --- Run --------------------------------------------------------------------
# shellcheck disable=SC1091
source venv/bin/activate
exec python dashboard/app.py
