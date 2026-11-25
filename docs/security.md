# Security (demo scope)

Local demo only. Not hardened for production or the public internet.

## Checklist sign-off

- [x] Admin password stored as **hash** only (`ADMIN_PASSWORD_HASH`)
- [x] CSRF on login, logout, and add-server forms (Flask-WTF)
- [x] Auth required on dashboard, add server, detail, and metrics APIs
- [x] Only `/login` and static assets are public
- [x] Generic login failure message (`Invalid credentials`)
- [x] Session cookies: `HttpOnly`, `SameSite=Lax` (HTTP local demo — `Secure` off)
- [x] `.gitignore` covers `.env`, venv, local `data/`, DBs
- [x] `DEBUG` off by default (no stack traces in browser)
- [x] Basic headers: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, CSP
- [x] Metrics are pure mocks — no SSH, no `/proc`, no shell

## Scope limits

- No HTTPS
- Bind `0.0.0.0:5777` exposes the demo on network interfaces — trusted LAN / local only
- Do **not** reuse the demo password elsewhere
- Mock data only — not real host telemetry
