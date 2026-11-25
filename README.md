# Monitoring Demo

Local demo web app for glancing at mock Linux server metrics (CPU, memory, network, listening ports) without logging into each host.

- PRD: [docs/requirements.md](docs/requirements.md)
- Checklist: [docs/TODO.md](docs/TODO.md)
- Security: [docs/security.md](docs/security.md)
- Testing: [docs/testing.md](docs/testing.md)
- CI: [docs/ci.md](docs/ci.md)

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

Binds to **`0.0.0.0:5777`** (all interfaces — local demo only).

- http://localhost:5777
- http://0.0.0.0:5777

Unauthenticated visitors are redirected to `/login`.

## Authentication config

| Setting | Default | Notes |
|---------|---------|--------|
| Username | `admin` | Override with `ADMIN_USERNAME` |
| Password | local demo value `demo` | **Hash only** is stored; do not reuse elsewhere |
| Hash | `ADMIN_PASSWORD_HASH` | Env override or default in `app/config.py` |
| `SECRET_KEY` | env or weak demo fallback | Set via environment / `.env` (see `.env.example`) |

Generate a new hash:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

Passwords are never logged. Verification uses werkzeug’s constant-time `check_password_hash`.

### Sign-in / logout

1. Open `/login`, submit username + password (POST + CSRF).
2. On success, a session is created and you land on the dashboard (`/`).
3. Logout (header) POSTs to `/logout` and clears the session.

## Add a server

1. Sign in → **Add server** (`/servers/add`).
2. Enter **Server name** and **Hostname / IP** only (no SSH credentials).
3. Duplicate hostname/IP is rejected. On success you return to the dashboard.

Server list is stored as JSON under `data/servers.json` (gitignored). Reset demo data by deleting that file (or the `data/` directory).

## Dashboard & detail

- **Dashboard (`/`):** lists servers with live mock CPU / memory / network (JSON refresh every **5 seconds**).
- **Detail (`/servers/<id>`):** CPU, memory, network, listening ports + process names (5s refresh).
- Metrics are **mock/sample only** — no real collectors or SSH.

### Metrics API (auth required)

| Endpoint | Response |
|----------|----------|
| `GET /api/dashboard` | `{ "servers": [ { id, name, host, cpu_percent, memory, network } ] }` |
| `GET /api/servers/<id>` | Same fields plus `listening_ports: [{ port, protocol, process }]` (404 if unknown) |

Example mock detail shape:

```json
{
  "id": "...",
  "name": "web-1",
  "host": "10.0.0.5",
  "cpu_percent": 42.1,
  "memory": { "used_mb": 1800.0, "total_mb": 4096, "percent": 44.0 },
  "network": { "in_mbps": 12.3, "out_mbps": 4.5 },
  "listening_ports": [
    { "port": 22, "protocol": "tcp", "process": "sshd" }
  ]
}
```

## Routes & auth

| Route | Auth |
|-------|------|
| `/login` | Public |
| Static (`/static/...`) | Public |
| `/`, `/logout`, `/servers/add`, `/servers/<id>` | Required |
| `/api/dashboard`, `/api/servers/<id>` | Required |

## UI overview

- Dark, simple theme: header, content, footer
- Templates: `app/templates/`
- Styles: `app/static/css/style.css`
- Client refresh: `app/static/js/` (same-origin session cookies only; no credentials in JS)
- Monitoring views are read-only (no edit/delete of metrics)

## Tests

```bash
pytest
```

See [docs/testing.md](docs/testing.md).

## CI

GitHub Actions runs lint (`ruff`), `pytest`, and a `/login` smoke check. Details: [docs/ci.md](docs/ci.md).

## Demo script (reviewers)

1. Start the app (`python -m app.main`) and open http://localhost:5777
2. Sign in as `admin` with the local demo password (`demo` unless you changed the hash)
3. Add a server (name + hostname/IP) and confirm it appears on the dashboard
4. Wait ~5s and confirm summary metrics refresh; open a server for ports/process
5. Logout and confirm the dashboard redirects to login

## Security notes

- Secrets, `.env`, and `data/` are gitignored — never commit credentials
- `0.0.0.0` exposes the demo on the network interface — trusted local use only
- Full checklist: [docs/security.md](docs/security.md)
