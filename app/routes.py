"""HTTP routes for the Monitoring Demo."""

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from app.auth import (
    is_authenticated,
    login_required,
    login_user,
    logout_user,
    verify_credentials,
)
from app.forms import AddServerForm, LoginForm
from app.metrics import generate_detail, generate_summary
from app.store import DuplicateHostError, add_server, get_server, list_servers

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def home():
    """Dashboard: registered servers (auth required)."""
    servers = list_servers()
    return render_template("dashboard.html", servers=servers)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if is_authenticated():
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        if verify_credentials(form.username.data, form.password.data):
            login_user()
            return redirect(url_for("main.home"))
        flash("Invalid credentials", "error")
    return render_template("login.html", form=form)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/servers/add", methods=["GET", "POST"])
@login_required
def servers_add():
    form = AddServerForm()
    if form.validate_on_submit():
        try:
            add_server(form.name.data, form.host.data)
            flash("Server added.", "success")
            return redirect(url_for("main.home"))
        except DuplicateHostError:
            form.host.errors.append(
                "A server with this hostname/IP already exists."
            )
    return render_template("server_add.html", form=form)


@bp.route("/servers/<server_id>")
@login_required
def server_detail(server_id: str):
    server = get_server(server_id)
    if server is None:
        return render_template("404.html", message="Server not found."), 404
    return render_template("server_detail.html", server=server)


@bp.route("/api/dashboard")
@login_required
def api_dashboard():
    """Auth-protected JSON summary for dashboard auto-refresh."""
    payload = []
    for server in list_servers():
        summary = generate_summary(server["id"])
        payload.append(
            {
                "id": server["id"],
                "name": server["name"],
                "host": server["host"],
                **summary,
            }
        )
    return jsonify({"servers": payload})


@bp.route("/api/servers/<server_id>")
@login_required
def api_server_detail(server_id: str):
    server = get_server(server_id)
    if server is None:
        return jsonify({"error": "not_found"}), 404
    detail = generate_detail(server_id)
    return jsonify(
        {
            "id": server["id"],
            "name": server["name"],
            "host": server["host"],
            **detail,
        }
    )


@bp.app_errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "not_found"}), 404
    return render_template("404.html", message="Page not found."), 404
