# Deploy — reviving the companion from scratch

The dashboard is a **self-contained Dash/gunicorn app**: no database, no external
API at run-time, all data embedded in the source → fully stateless. Nothing to
migrate. WSGI entry point: **`app:server`** (module-level `server = app.server`
in `dashboard/app.py`). Local port `8082`.

## 1. Run locally

```bash
python3.12 -m venv venv
venv/bin/pip install -r requirements.txt
./run-api.sh        # debug reloader on 0.0.0.0:8082
# production-style:
# venv/bin/gunicorn --chdir dashboard --bind 0.0.0.0:8082 --workers 1 --threads 4 app:server
```

## 2. Production — DigitalOcean App Platform (current)

Python buildpack + the repo `Procfile`. Reference spec: **`.do/app.yaml`**.

- **Panel:** Create App → GitHub → repo `IMHOIT-SL/gratacos-botto`, branch `main`
  → it detects Python + `Procfile`. Plan: **Basic XXS (512 MB, $5/mo)**.
- **Run command** (1 worker fits 512 MB; 2 OOM with pandas/statsmodels):
  ```
  gunicorn --chdir dashboard --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:server
  ```
- **Custom domain:** add `resistome.imhoit.com`; in Cloudflare set a **DNS-only**
  (grey) CNAME → `<app>.ondigitalocean.app`. DO issues the TLS cert. (DO apps sit
  behind DO's own Cloudflare edge, so responses show `cf-ray` even DNS-only.)
- **Deploy = `git push` to `main`** → GitHub webhook → DO auto-redeploys (~1.5 min).
- **CLI alt:** `doctl apps create --spec .do/app.yaml`. Note: `doctl` is a **snap**
  and cannot read `/tmp` — keep spec files under `$HOME`.

## 3. Fallback — self-host behind a Cloudflare Tunnel

See **`deploy/systemd/INSTALL.md`**. Runs gunicorn + a `cloudflared` tunnel as
services (system units, or user units via `systemctl --user` + `loginctl
enable-linger`). Requires the tunnel credentials in `~/.cloudflared/` — **NOT in
this repo** (secrets). Never touch a pre-existing `/etc/cloudflared/` on a shared
host.
