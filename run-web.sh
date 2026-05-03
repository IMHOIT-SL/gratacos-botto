#!/usr/bin/env bash
# Cloudflare Tunnel launcher — exposes the local AMR Dashboard at
# https://resistome.imhoit.com via the dedicated 'resistome' tunnel.
# Stop with Ctrl+C. Independent of any other cloudflared service running on
# this host.

set -euo pipefail

TUNNEL_NAME="resistome"
TUNNEL_CONFIG="${HOME}/.cloudflared/${TUNNEL_NAME}.yml"
PUBLIC_URL="https://resistome.imhoit.com"
LOCAL_PORT="${PORT:-8082}"

# --- Sanity checks -----------------------------------------------------------
if ! command -v cloudflared >/dev/null 2>&1; then
    echo "ERROR: cloudflared not found in PATH"
    echo "  Install: see https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
    exit 1
fi

if [[ ! -f "$TUNNEL_CONFIG" ]]; then
    echo "ERROR: Tunnel config not found at $TUNNEL_CONFIG"
    echo "  Create it as documented in dashboard/docs/setup.md (Deployment section)."
    exit 1
fi

# Soft-check: confirm the API is reachable locally before exposing the tunnel.
api_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "http://127.0.0.1:${LOCAL_PORT}/" 2>/dev/null || echo "000")
if [[ "$api_status" != "200" ]]; then
    echo "WARNING: Dashboard at http://127.0.0.1:${LOCAL_PORT} returned HTTP ${api_status}."
    echo "  Run-api.sh in another terminal first, otherwise the tunnel will serve 502 errors."
    echo "  Continuing anyway in 3s..."
    sleep 3
fi

# --- Banner ------------------------------------------------------------------
cat <<EOF
─────────────────────────────────────────────────
  Cloudflare Tunnel — ${TUNNEL_NAME}
  Config:   $TUNNEL_CONFIG
  Routes:   $PUBLIC_URL  →  http://localhost:${LOCAL_PORT}
  Stop:     Ctrl+C
─────────────────────────────────────────────────
EOF

# --- Run --------------------------------------------------------------------
exec cloudflared tunnel --config "$TUNNEL_CONFIG" run "$TUNNEL_NAME"
