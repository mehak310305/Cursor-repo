"""Flask application factory for the Monitoring Demo."""

from flask import Flask

from app import config


def create_app() -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config)

    @app.after_request
    def set_security_headers(response):
        """Basic response headers for the local demo."""
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    from app.routes import bp

    app.register_blueprint(bp)
    return app
