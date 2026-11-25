# CI

GitHub Actions workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

## What runs

On push/PR to `main` / `master`:

1. Install pinned deps from `requirements.txt` (pip cache enabled)
2. `ruff check app tests`
3. `pytest` (job fails if tests fail)
4. Smoke: import Flask app and `GET /login` via test client (no long-lived server)
5. Optional `pip-audit` (`continue-on-error: true`)

## Security notes

- Workflow `permissions: contents: read`
- Dummy CI env for `SECRET_KEY` / password hash placeholders — no real secrets
- Action versions pinned (`actions/checkout@v4`, `actions/setup-python@v5`)
