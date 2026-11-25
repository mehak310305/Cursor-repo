"""Lightweight JSON store for registered servers (outside static/)."""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import current_app

_lock = threading.Lock()


def _path() -> Path:
    return Path(current_app.config["SERVERS_FILE"])


def _ensure_store() -> Path:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    return path


def _read_all() -> list[dict[str, Any]]:
    path = _ensure_store()
    with _lock:
        raw = path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = []
        if not isinstance(data, list):
            data = []
        return data


def _write_all(servers: list[dict[str, Any]]) -> None:
    path = _ensure_store()
    with _lock:
        path.write_text(
            json.dumps(servers, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )


def list_servers() -> list[dict[str, Any]]:
    return _read_all()


def get_server(server_id: str) -> dict[str, Any] | None:
    for server in _read_all():
        if server.get("id") == server_id:
            return server
    return None


def host_exists(host: str) -> bool:
    normalized = host.strip().lower()
    return any(s.get("host", "").strip().lower() == normalized for s in _read_all())


class DuplicateHostError(ValueError):
    """Raised when hostname/IP is already registered."""


def add_server(name: str, host: str) -> dict[str, Any]:
    name = name.strip()
    host = host.strip()
    servers = _read_all()
    if any(s.get("host", "").strip().lower() == host.lower() for s in servers):
        raise DuplicateHostError("A server with this hostname/IP already exists.")
    server = {
        "id": str(uuid.uuid4()),
        "name": name,
        "host": host,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    servers.append(server)
    _write_all(servers)
    return server


def reset_store() -> None:
    """Clear all servers (tests / demo reset)."""
    path = _ensure_store()
    with _lock:
        path.write_text("[]\n", encoding="utf-8")
