"""Serve the marketing site and the Expo web export at /app.

Extensionless Expo routes such as /app/game map to app/game.html.
Real files (scripts, images, favicon) are served as-is.
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        self._rewrite_app_route()
        super().do_GET()

    def do_HEAD(self):
        self._rewrite_app_route()
        super().do_HEAD()

    def _rewrite_app_route(self):
        raw, _, query = self.path.partition("?")
        if raw != "/app" and not raw.startswith("/app/"):
            return

        suffix = "" if raw in ("/app", "/app/") else raw[len("/app/") :]
        if suffix.endswith("/"):
            suffix = suffix[:-1]

        candidate = APP / suffix if suffix else APP
        if candidate.is_dir():
            rewritten = "/app/index.html" if not suffix else f"/app/{suffix}/index.html"
        elif candidate.is_file():
            return
        elif (APP / f"{suffix}.html").is_file():
            rewritten = f"/app/{suffix}.html"
        else:
            not_found = APP / "+not-found.html"
            rewritten = "/app/+not-found.html" if not_found.is_file() else raw

        self.path = rewritten if not query else f"{rewritten}?{query}"


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Serving http://127.0.0.1:8765/")
    server.serve_forever()
