"""Application entry point.

Run with:
    python -m app.main

Binds to 0.0.0.0:5777 (all interfaces — local demo only).
"""

from app import create_app
from app.config import DEBUG, HOST, PORT

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
