"""Authentication and route protection tests."""

from tests.conftest import TEST_PASSWORD


def test_login_success(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": TEST_PASSWORD},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_failure(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data


def test_logout(auth_client):
    response = auth_client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
    blocked = auth_client.get("/", follow_redirects=False)
    assert blocked.status_code == 302
    assert "/login" in blocked.headers["Location"]


def test_protected_route_redirects_anonymous(client):
    for path in ("/", "/servers/add", "/api/dashboard"):
        response = client.get(path, follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


def test_login_page_is_public(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data
