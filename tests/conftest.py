"""Shared pytest fixtures — test hashes only, no production secrets."""

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.store import reset_store

TEST_PASSWORD = "test-password-not-for-prod"
TEST_PASSWORD_HASH = generate_password_hash(TEST_PASSWORD)


@pytest.fixture()
def app(tmp_path):
    data_file = tmp_path / "servers.json"
    data_file.write_text("[]\n", encoding="utf-8")
    application = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret-key",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD_HASH": TEST_PASSWORD_HASH,
            "SERVERS_FILE": data_file,
            "DATA_DIR": tmp_path,
        }
    )
    yield application
    with application.app_context():
        reset_store()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_client(client):
    client.post(
        "/login",
        data={"username": "admin", "password": TEST_PASSWORD},
        follow_redirects=False,
    )
    return client
