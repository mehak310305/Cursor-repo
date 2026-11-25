# TODO: Demo Monitoring Infrastructure

Incremental implementation checklist aligned with [requirements.md](./requirements.md).  
Work **one checkbox group at a time**. Each step includes **security** and **docs**.

---

## Phase 0 — Project initialization & basic UI

### 0.1 Repo skeleton
- [x] Create project layout: `app/`, `tests/`, `docs/`, `.github/workflows/`
- [x] Add `.gitignore` (Python, venv, `__pycache__`, `.env`, IDE files, local DB/JSON data)
- [x] **Security:** Ensure secrets, `.env`, and local data files are ignored; never commit credentials
- [x] **Docs:** Add stub `README.md` with project name and one-line purpose

### 0.2 Dependencies & app entry
- [x] Add `requirements.txt` with Flask (pin versions)
- [x] Create minimal Flask app (`app/__init__.py` or `app/main.py`) that serves a home route
- [x] Bind the app to **`0.0.0.0`** on port **`5777`** (e.g. `app.run(host="0.0.0.0", port=5777)`)
- [x] **Security:** Do not hardcode secrets; use a placeholder config module with no real passwords yet; note that `0.0.0.0` exposes the demo on the network interface—local demo only
- [x] **Docs:** Document `python -m venv`, activate, `pip install -r requirements.txt`, and how to run the app at `http://0.0.0.0:5777` / `http://localhost:5777`

### 0.3 Basic dark UI shell
- [x] Add base HTML template + dark CSS (simple modern layout: header, content area)
- [x] Render a static “Monitoring Demo” landing/placeholder page
- [x] **Security:** Set `X-Frame-Options` / basic response headers if trivial; avoid inline third-party scripts from untrusted CDNs unless needed
- [x] **Docs:** Note UI theme (dark, simple) and template locations in README

---

## Phase 1 — Sign-in & unit tests

### 1.1 Config for admin auth
- [x] Add config for `ADMIN_USERNAME=admin` and a **hashed** password (werkzeug/passlib hash)
- [x] Load `SECRET_KEY` from environment or local config file (not committed with production values)
- [x] **Security:** Store only password **hash**; document how to generate the hash; never log passwords
- [x] **Docs:** Add “Authentication config” section (username, hashing, env vars)

### 1.2 Login page UI
- [x] Add `/login` route + form (username, password, submit)
- [x] Style login to match dark UI; link unauthenticated home → login
- [x] **Security:** Use POST for credentials; CSRF protection (Flask-WTF or equivalent); autocomplete-friendly password field
- [x] **Docs:** Document login URL and default username (not the password value in git if avoidable—point to local config)

### 1.3 Session-based sign-in / logout
- [x] Verify username + hashed password; create session on success; redirect to dashboard placeholder
- [x] Add logout that clears session; reject invalid credentials with generic error message
- [x] **Security:** Generic failure message (“Invalid credentials”); secure session cookie flags for local demo (`HttpOnly`, `SameSite`); constant-time hash check via library
- [x] **Docs:** Document sign-in / logout flow in README

### 1.4 Auth unit tests
- [x] Add `pytest` (+ Flask test client) to requirements/dev deps
- [x] Tests: login success, login failure, logout, protected route redirects when anonymous
- [x] **Security:** Tests must use test config hashes—no production secrets in tests
- [x] **Docs:** Document how to run tests: `pytest`

### 1.5 Protect routes
- [x] Add login-required decorator/middleware for non-login pages
- [x] Redirect anonymous users to `/login`
- [x] **Security:** Ensure only `/login` (and static assets) are public
- [x] **Docs:** List which routes require auth

---

## Phase 2 — Server registry (name + host)

### 2.1 Data store for servers
- [x] Choose lightweight store (SQLite or JSON file under a local data path)
- [x] Model: id, name, hostname/IP, created_at
- [x] **Security:** Validate/sanitize name and host input length; path for DB/JSON outside web-accessible static dirs
- [x] **Docs:** Document storage location and how to reset demo data

### 2.2 Add-server form
- [x] Add `/servers/add` (GET form + POST submit): fields **Server name**, **Hostname/IP** only
- [x] On success, redirect to dashboard; show validation errors inline
- [x] **Security:** CSRF on form; reject empty/oversized fields; basic hostname/IP format check
- [x] **Docs:** Document how to add a server

### 2.3 Duplicate host handling
- [x] Reject or clearly flag duplicate hostname/IP
- [x] Unit tests for add success + duplicate rejection
- [x] **Security:** Do not reflect raw unsanitized input in error HTML (escape templates)
- [x] **Docs:** Note duplicate rule in README / requirements cross-link

### 2.4 List servers on dashboard shell
- [x] Dashboard route lists registered servers (name + host); link to detail placeholder
- [x] Empty state when no servers
- [x] **Security:** Auth-only access; autoescape templates (Jinja default)
- [x] **Docs:** Screenshot or short description of dashboard empty vs populated

---

## Phase 3 — Mock metrics engine

### 3.1 Mock metric generator
- [x] Module that returns plausible CPU %, memory used/total/%, network in/out
- [x] Slight variance per call to simulate “live” data
- [x] **Security:** No OS/shell calls; pure mock—avoid accidental real probing APIs
- [x] **Docs:** Document that metrics are **mock/sample only**

### 3.2 Listening ports mock
- [x] Generator returns list of listening ports with **process name** (and protocol if trivial)
- [x] Unit tests for shape/ranges of mock payloads
- [x] **Security:** Fixed allowlist of fake process names; no reading real `/proc`
- [x] **Docs:** Example mock JSON shape in docs or README

### 3.3 Metrics API for UI refresh
- [x] Auth-protected JSON endpoint(s) for dashboard summary and server detail
- [x] Return 404 for unknown server id
- [x] **Security:** Auth required on API; no sensitive config in JSON responses
- [x] **Docs:** Document endpoint paths and response fields

---

## Phase 4 — Dashboard & server detail UI

### 4.1 Dashboard live summary
- [x] Show per-server CPU, memory, network summary on dashboard
- [x] Client auto-refresh every **5 seconds** (fetch JSON or reload partial)
- [x] **Security:** Credentials not stored in JS; fetch with same-origin session cookies only
- [x] **Docs:** Note 5s refresh behavior

### 4.2 Server detail page
- [x] `/servers/<id>` shows CPU, memory, network, listening ports + process names
- [x] Auto-refresh every **5 seconds**; back link to dashboard
- [x] **Security:** Auth-only; validate `id`; 404 for missing; escape all rendered fields
- [x] **Docs:** Document detail page fields

### 4.3 UI polish (dark, read-only)
- [x] Consistent dark theme, readable tables/cards for metrics (keep simple)
- [x] Monitoring views remain read-only (no edit/delete metrics)
- [x] **Security:** No dangerous HTML from mock data; CSP-friendly structure if easy
- [x] **Docs:** Update README “UI overview”

### 4.4 Feature tests
- [x] Tests: dashboard requires login; detail requires login; add server then see it listed; metrics JSON shape
- [x] **Security:** Confirm anonymous access denied for dashboard, detail, metrics API, add-server
- [x] **Docs:** List test coverage areas in README or `docs/testing.md`

---

## Phase 5 — CI/CD (GitHub Actions)

### 5.1 Workflow: lint & test
- [x] Add `.github/workflows/ci.yml` — on push/PR: install deps, run `pytest`
- [x] Optionally run a lightweight linter (e.g. `ruff` or `flake8`)
- [x] **Security:** No secrets in workflow logs; use dummy test password hash in CI env; pin action versions (`@v4` etc.)
- [x] **Docs:** Document CI status badge and what the pipeline runs

### 5.2 Dependency / safety hygiene in CI
- [x] Cache pip dependencies; fail job on test failure
- [x] Optional: `pip audit` or safety check as non-blocking or blocking step
- [x] **Security:** Least-privilege `permissions:` on the workflow (e.g. `contents: read`)
- [x] **Docs:** Short `docs/ci.md` or README section explaining CI

### 5.3 Smoke check (optional, still small)
- [x] CI step that imports the Flask app / hits `/login` with test client
- [x] **Security:** Do not start a long-lived public server in CI
- [x] **Docs:** Note smoke check in CI docs

---

## Phase 6 — Hardening & demo readiness

### 6.1 Final security pass
- [x] Review: hashed password only, CSRF on forms, auth on all sensitive routes, `.gitignore` complete
- [x] Ensure error messages do not leak stack traces in demo “production-like” config (`DEBUG` off by default)
- [x] **Security:** Checklist sign-off in docs
- [x] **Docs:** Add `docs/security.md` (demo scope: local-only, mock data, no HTTPS)

### 6.2 Final documentation pass
- [x] Complete README: setup, run, login, add server, dashboard, tests, CI
- [x] Link README ↔ `docs/requirements.md` ↔ `docs/TODO.md`
- [x] **Security:** Remind users not to reuse the demo password elsewhere
- [x] **Docs:** Mark TODO items done as work completes; keep requirements as source of truth

### 6.3 Local demo verification
- [x] Confirm app listens on **`0.0.0.0:5777`**
- [x] Manual walkthrough: open `:5777` → login → add server → dashboard 5s refresh → server detail ports/process
- [x] Confirm non-goals still out of scope (no alerts, HTTPS, real collectors)
- [x] **Security:** Confirm logout clears access to dashboard
- [x] **Docs:** Add a short “Demo script” (3–5 steps) for L1/L2/L3 reviewers

---

## Suggested order (AI-assisted)

1. Phase 0 (init + basic UI)  
2. Phase 1 (sign-in + unit tests)  
3. Phase 2 (add/list servers)  
4. Phase 3 (mock metrics)  
5. Phase 4 (live UI)  
6. Phase 5 (GitHub Actions CI)  
7. Phase 6 (security + docs wrap-up)

Do not skip security or docs checkboxes within a step.
