# systemd deployment — resistome

Two independent units that auto-start at boot and auto-restart on crash:

| Unit                                | What it does                                         |
|-------------------------------------|------------------------------------------------------|
| `resistome-dashboard.service`       | gunicorn on `127.0.0.1:8082` (the Dash app)         |
| `cloudflared-resistome.service`     | Cloudflare Tunnel → `resistome.imhoit.com`           |

Both run as `User=ia`. Independent of the existing root-owned `cloudflared.service` (chat-tunnel) — they coexist by design.

## Install

```bash
# 1. Stop any manual run-api.sh / run-web.sh sessions first.

# 2. Copy unit files into /etc/systemd/system/
sudo cp deploy/systemd/resistome-dashboard.service /etc/systemd/system/
sudo cp deploy/systemd/cloudflared-resistome.service /etc/systemd/system/

# 3. Reload systemd, enable on boot, start now.
sudo systemctl daemon-reload
sudo systemctl enable --now resistome-dashboard.service
sudo systemctl enable --now cloudflared-resistome.service

# 4. Verify
systemctl status resistome-dashboard.service cloudflared-resistome.service --no-pager
curl -sI http://127.0.0.1:8082/ | head -1
curl -sI https://resistome.imhoit.com/ | head -1
```

## Logs

```bash
journalctl -u resistome-dashboard.service -f
journalctl -u cloudflared-resistome.service -f
```

## Restart / stop

```bash
sudo systemctl restart resistome-dashboard.service
sudo systemctl stop resistome-dashboard.service cloudflared-resistome.service
```

## Uninstall (does NOT touch chat-tunnel cloudflared.service)

```bash
sudo systemctl disable --now resistome-dashboard.service cloudflared-resistome.service
sudo rm /etc/systemd/system/resistome-dashboard.service
sudo rm /etc/systemd/system/cloudflared-resistome.service
sudo systemctl daemon-reload
```

## What's NOT touched

- `/etc/cloudflared/config.yml` (chat-tunnel config — root-owned)
- `cloudflared.service` (chat-tunnel systemd unit — root-owned)
- `~/.cloudflared/` files for other tunnels (atlas-dev, etc.)
