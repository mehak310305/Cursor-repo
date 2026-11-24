# PRD: Demo Monitoring Infrastructure (Linux Servers)

## 1. Overview

A local demo web app for monitoring Linux servers. Users view live CPU, memory, network, and listening-port metrics without logging into each server.

**Audience:** Internal L1 / L2 / L3 and application teams (read-only demo).  
**Deployment:** Local machine only (where Cursor runs).  
**Bind:** `0.0.0.0:5777` (listen on all interfaces, port **5777**).  
**Data:** Mock/sample metrics (no real SSH or agents).

## 2. Goals

- Replace ad-hoc server logins for a quick glance at resource and port usage.
- Provide a simple, dark, modern read-only UI.
- Keep setup and scope minimal for a local demo.

## 3. Non-Goals

- Real metric collection, agents, or SSH
- Historical charts or retention
- Alerts, email, or notifications
- Multi-user roles or multi-tenancy
- HTTPS / production hardening
- Disk, process lists beyond listening ports, or export/reporting

## 4. Users & Access

| Item | Detail |
|------|--------|
| Users | Single shared admin account |
| Username | `admin` (default) |
| Password | Fixed value stored hashed in config |
| Mode | Read-only UI after login (no destructive actions) |

## 5. User Flows

1. **Sign in** → enter `admin` + password → land on Dashboard.
2. **Dashboard** → see all registered servers and live summary metrics (auto-refresh every 5s).
3. **Add server** → enter server name + hostname/IP → server appears on Dashboard.
4. **Server detail** → open a server → view CPU, memory, network, and listening ports with process names (refresh every 5s).

## 6. Features

### 6.1 Authentication

- Login page with username and password.
- Default username: `admin`.
- Password verified against a hashed value in application config (not plain text).
- Unauthenticated users redirected to login.
- Session ends on logout or browser close (simple session is enough).

### 6.2 Add Servers

- Form fields: **Server name**, **Hostname / IP** only.
- No SSH credentials (mock data).
- Added servers listed on the Dashboard.
- Duplicate hostname/IP should be rejected or clearly indicated.

### 6.3 Dashboard (read-only)

- List of monitored servers with name and hostname/IP.
- Per-server live summary: CPU %, memory %, network in/out (mock).
- Auto-refresh every **5 seconds**.
- Click a server to open Server Detail.
- Dark, simple, modern layout.

### 6.4 Server Detail (read-only)

Live mock metrics, refreshed every **5 seconds**:

| Metric | Display |
|--------|---------|
| CPU | Usage % |
| Memory | Used / total and % |
| Network | Inbound and outbound throughput |
| Listening ports | Port, protocol (if available), process name |

No history, charts over time, or stored metric series.

### 6.5 Mock Data

- App generates plausible sample values for CPU, memory, network, and listening ports.
- Values may vary slightly on each refresh to simulate live monitoring.
- Mock data is sufficient; no connection to real hosts required.

## 7. Tech Stack

| Layer | Choice |
|-------|--------|
| Language | Python |
| Web framework | Flask |
| UI | Attractive dark modern dashboard (HTML/CSS/JS served by Flask) |
| Auth secret | Hashed admin password in config |
| Persistence | Lightweight local store for server list (e.g. SQLite or JSON file) |

## 8. Pages

| Route (conceptual) | Purpose |
|--------------------|---------|
| `/login` | Sign in |
| `/` or `/dashboard` | Server list + summary metrics |
| `/servers/add` | Add server (name + host) |
| `/servers/<id>` | Server detail metrics |

All pages except login require an authenticated session. UI is read-only aside from login and adding servers.

## 9. Functional Requirements (minimal)

1. User can sign in with `admin` and the configured password.
2. User can add a Linux server by name and hostname/IP.
3. Dashboard shows all servers with live mock summaries every 5s.
4. Server detail shows CPU, memory, network, and listening ports (with process name) every 5s.
5. UI is dark, modern, and read-only for monitoring views.

## 10. Out of Scope (demo)

Alerts, email, HTTPS, real collectors, history, multi-admin, roles, password change UI, server edit/delete (optional later), mobile-first polish.

## 11. Local Run (minimal)

```text
1. Install Python dependencies
2. Set/config hashed admin password in config
3. Run Flask app bound to 0.0.0.0 on port 5777
4. Open browser → http://<host>:5777 → login as admin → add servers → view dashboard/detail
```

Exact commands and package list belong in a README during implementation, not here.

**Runtime bind (required):** `host=0.0.0.0`, `port=5777`.

## 12. Success Criteria

- Local demo runs without external servers or agents.
- L1/L2/L3-style users can log in and view live mock metrics without SSH.
- Adding a server requires only name + hostname/IP.
- UI refreshes every 5 seconds and matches a dark, simple dashboard look.
