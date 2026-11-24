"""Application configuration placeholders.

No real passwords or production secrets live here.
Auth hashing and SECRET_KEY from the environment will be added in Phase 1.
"""

# Demo bind address — 0.0.0.0 exposes the app on all interfaces (local demo only).
HOST = "0.0.0.0"
PORT = 5777

# DEBUG stays off by default for safer local demos.
DEBUG = False

# Placeholder only — replace via environment / local config in Phase 1.
SECRET_KEY = "change-me-demo-only"
