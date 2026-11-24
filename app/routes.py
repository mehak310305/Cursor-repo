"""HTTP routes for the Monitoring Demo."""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    """Static landing / placeholder page."""
    return render_template("home.html")
