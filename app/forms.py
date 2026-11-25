"""WTForms with CSRF for login and add-server."""

import ipaddress
import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app import config

# Hostname: labels with letters/digits/hyphen; optional trailing dot.
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)


def _valid_host(value: str) -> bool:
    value = value.strip()
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        pass
    return bool(_HOSTNAME_RE.match(value))


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=64)],
        render_kw={"autocomplete": "username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(max=256)],
        render_kw={"autocomplete": "current-password"},
    )
    submit = SubmitField("Sign in")


class AddServerForm(FlaskForm):
    name = StringField(
        "Server name",
        validators=[
            DataRequired(message="Server name is required."),
            Length(max=config.SERVER_NAME_MAX_LEN),
        ],
    )
    host = StringField(
        "Hostname / IP",
        validators=[
            DataRequired(message="Hostname / IP is required."),
            Length(max=config.SERVER_HOST_MAX_LEN),
        ],
    )
    submit = SubmitField("Add server")

    def validate_host(self, field):
        if not _valid_host(field.data or ""):
            raise ValidationError("Enter a valid hostname or IP address.")
