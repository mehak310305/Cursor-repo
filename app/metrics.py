"""Pure mock metrics — no OS/shell calls, no real host probing."""

from __future__ import annotations

import hashlib
import random
from typing import Any

# Fixed allowlist of fake process names (never read from /proc).
_FAKE_PROCESSES = (
    "sshd",
    "nginx",
    "systemd",
    "docker-proxy",
    "postgres",
    "redis-server",
    "node",
    "python3",
)


def _rng_for(seed: str) -> random.Random:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def generate_summary(server_id: str) -> dict[str, Any]:
    """Plausible CPU / memory / network with slight variance per call."""
    base = _rng_for(server_id)
    # Mix a time-ish variance without wall-clock coupling for tests: use random.
    jitter = random.Random()
    cpu = round(min(99.0, max(1.0, base.uniform(8, 72) + jitter.uniform(-4, 4))), 1)
    mem_total_mb = base.choice([2048, 4096, 8192, 16384])
    mem_pct = round(min(95.0, max(5.0, base.uniform(20, 80) + jitter.uniform(-3, 3))), 1)
    mem_used_mb = round(mem_total_mb * mem_pct / 100.0, 1)
    net_in = round(max(0.1, base.uniform(0.5, 40) + jitter.uniform(-2, 2)), 2)
    net_out = round(max(0.1, base.uniform(0.5, 30) + jitter.uniform(-2, 2)), 2)
    return {
        "cpu_percent": cpu,
        "memory": {
            "used_mb": mem_used_mb,
            "total_mb": mem_total_mb,
            "percent": mem_pct,
        },
        "network": {
            "in_mbps": net_in,
            "out_mbps": net_out,
        },
    }


def generate_listening_ports(server_id: str) -> list[dict[str, Any]]:
    """Listening ports with process name from a fixed fake allowlist."""
    rng = _rng_for(f"ports:{server_id}")
    count = rng.randint(3, 6)
    ports: list[dict[str, Any]] = []
    used = set()
    common = [22, 80, 443, 5432, 6379, 8080, 3000, 9090]
    for _ in range(count):
        if common and rng.random() < 0.7:
            port = common.pop(rng.randrange(len(common)))
        else:
            port = rng.randint(1024, 65535)
        if port in used:
            continue
        used.add(port)
        ports.append(
            {
                "port": port,
                "protocol": rng.choice(["tcp", "tcp6"]),
                "process": rng.choice(_FAKE_PROCESSES),
            }
        )
    ports.sort(key=lambda p: p["port"])
    return ports


def generate_detail(server_id: str) -> dict[str, Any]:
    summary = generate_summary(server_id)
    summary["listening_ports"] = generate_listening_ports(server_id)
    return summary
