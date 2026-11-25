"""Server registry tests."""


def test_add_server_success(auth_client):
    response = auth_client.post(
        "/servers/add",
        data={"name": "web-1", "host": "10.0.0.5"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    dashboard = auth_client.get("/")
    assert b"web-1" in dashboard.data
    assert b"10.0.0.5" in dashboard.data


def test_duplicate_host_rejected(auth_client):
    auth_client.post(
        "/servers/add",
        data={"name": "first", "host": "db.example.com"},
    )
    response = auth_client.post(
        "/servers/add",
        data={"name": "second", "host": "db.example.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"already exists" in response.data


def test_add_server_requires_login(client):
    response = client.get("/servers/add", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_invalid_host_rejected(auth_client):
    response = auth_client.post(
        "/servers/add",
        data={"name": "bad", "host": "not a host!!!"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"valid hostname" in response.data
