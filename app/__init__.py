"""Flask application factory for the Monitoring Demo."""

from flask import Flask
from flask_wtf import CSRFProtect

from app import config

csrf = CSRFProtect()


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config)
    if test_config:
        app.config.update(test_config)

    csrf.init_app(app)

    @app.after_request
    def set_security_headers(response):
        """Basic response headers for the local demo."""
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self'; "
            "script-src 'self'; "
            "img-src 'self' data:; "
            "frame-ancestors 'none'"
        )
        return response

    from app.routes import bp

    app.register_blueprint(bp)
    return app
