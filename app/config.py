"""Application configuration.

Demo defaults are for local use only. Prefer SECRET_KEY from the environment.
Never commit production secrets. Store only password hashes — never plaintext.

Generate a new admin password hash:
    python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
Then set ADMIN_PASSWORD_HASH (env) or update the default below.
"""

import os
from pathlib import Path

# Demo bind address — 0.0.0.0 exposes the app on all interfaces (local demo only).
HOST = "0.0.0.0"
PORT = 5777

# DEBUG stays off by default so stack traces are not shown to browsers.
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

# Prefer env; demo fallback is intentionally weak — change for anything shared.
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-demo-only-not-for-reuse")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")

# Hash for local demo password "demo" (do not reuse this password elsewhere).
# Override with ADMIN_PASSWORD_HASH in the environment for a custom password.
_DEFAULT_ADMIN_PASSWORD_HASH = (
    "scrypt:32768:8:1$zS00Lrko44EWiHZM$"
    "121e618ec7abb57e0c5f471286ec6dc2429f7a9feb4274b47bdf09413ba668d9"
    "09ab4b8be8f743b5a190ada1e9d052fc2150b38d35463149d3db52a74c6a7c06"
)
ADMIN_PASSWORD_HASH = os.environ.get(
    "ADMIN_PASSWORD_HASH", _DEFAULT_ADMIN_PASSWORD_HASH
)

# Session cookie flags for local HTTP demo (Secure=False so cookies work without HTTPS).
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False

# CSRF (Flask-WTF)
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Server registry JSON lives outside web-accessible static dirs.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("MONITORING_DATA_DIR", BASE_DIR / "data"))
SERVERS_FILE = DATA_DIR / "servers.json"

# Field limits for server registry
SERVER_NAME_MAX_LEN = 64
SERVER_HOST_MAX_LEN = 253
