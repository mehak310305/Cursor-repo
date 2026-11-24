# Monitoring Demo

Local demo web app for glancing at mock Linux server metrics (CPU, memory, network, listening ports) without logging into each host.

See [docs/requirements.md](docs/requirements.md) for the full PRD and [docs/TODO.md](docs/TODO.md) for the implementation checklist.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

The app binds to **`0.0.0.0:5777`** (all network interfaces — intended for local demo only).

- http://localhost:5777
- http://0.0.0.0:5777

## UI

- **Theme:** Dark, simple layout (header + content + footer).
- **Templates:** `app/templates/` (`base.html`, `home.html`)
- **Styles:** `app/static/css/style.css` (self-hosted; no third-party CDNs)

## Security notes (Phase 0)

- Secrets, `.env`, and local data files are listed in `.gitignore` — never commit credentials.
- Config placeholders live in `app/config.py` (no real passwords yet).
- Binding to `0.0.0.0` exposes the demo on the machine’s network interfaces; use only on trusted local networks.
- Responses include basic headers: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`.
