"""Authentication helpers and login-required protection."""

from functools import wraps

from flask import current_app, redirect, session, url_for
from werkzeug.security import check_password_hash


def verify_credentials(username: str, password: str) -> bool:
    """Constant-time hash check via werkzeug; never log the password."""
    expected_user = current_app.config["ADMIN_USERNAME"]
    password_hash = current_app.config["ADMIN_PASSWORD_HASH"]
    if username != expected_user:
        # Still run hash check to avoid trivial username timing hints.
        check_password_hash(password_hash, password)
        return False
    return check_password_hash(password_hash, password)


def login_user() -> None:
    session.clear()
    session["authenticated"] = True
    session["username"] = current_app.config["ADMIN_USERNAME"]


def logout_user() -> None:
    session.clear()


def is_authenticated() -> bool:
    return bool(session.get("authenticated"))


def login_required(view):
    """Redirect anonymous users to /login."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped
