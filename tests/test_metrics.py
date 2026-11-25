"""Mock metrics shape and API tests."""

from app.metrics import generate_detail, generate_summary


def test_summary_shape_and_ranges():
    summary = generate_summary("server-abc")
    assert 0 < summary["cpu_percent"] <= 100
    mem = summary["memory"]
    assert mem["total_mb"] > 0
    assert 0 < mem["percent"] <= 100
    assert 0 <= mem["used_mb"] <= mem["total_mb"]
    net = summary["network"]
    assert net["in_mbps"] >= 0
    assert net["out_mbps"] >= 0


def test_listening_ports_use_allowlist():
    detail = generate_detail("server-xyz")
    ports = detail["listening_ports"]
    assert isinstance(ports, list)
    assert ports
    allowed = {
        "sshd",
        "nginx",
        "systemd",
        "docker-proxy",
        "postgres",
        "redis-server",
        "node",
        "python3",
    }
    for entry in ports:
        assert 1 <= entry["port"] <= 65535
        assert entry["protocol"] in {"tcp", "tcp6"}
        assert entry["process"] in allowed


def test_metrics_api_requires_auth(client):
    response = client.get("/api/dashboard", follow_redirects=False)
    assert response.status_code == 302


def test_dashboard_metrics_json(auth_client):
    auth_client.post(
        "/servers/add",
        data={"name": "api-box", "host": "192.168.1.10"},
    )
    response = auth_client.get("/api/dashboard")
    assert response.status_code == 200
    payload = response.get_json()
    assert "servers" in payload
    assert len(payload["servers"]) == 1
    row = payload["servers"][0]
    assert "cpu_percent" in row
    assert "memory" in row
    assert "network" in row


def test_server_detail_api_404(auth_client):
    response = auth_client.get("/api/servers/does-not-exist")
    assert response.status_code == 404


def test_server_detail_page_requires_login(client):
    response = client.get("/servers/some-id", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_detail_page_after_add(auth_client):
    auth_client.post(
        "/servers/add",
        data={"name": "detail-box", "host": "host.internal"},
    )
    listing = auth_client.get("/api/dashboard").get_json()
    server_id = listing["servers"][0]["id"]
    page = auth_client.get(f"/servers/{server_id}")
    assert page.status_code == 200
    assert b"detail-box" in page.data
    api = auth_client.get(f"/api/servers/{server_id}")
    assert api.status_code == 200
    body = api.get_json()
    assert "listening_ports" in body
