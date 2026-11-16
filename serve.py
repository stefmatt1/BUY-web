"""Serve the marketing site and the Expo web export at /score-tracker.

Extensionless Expo routes such as /score-tracker/game map to score-tracker/game.html.
Real files (scripts, images, favicon) are served as-is.
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "score-tracker"
PREFIX = "/score-tracker"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        self._rewrite_tracker_route()
        super().do_GET()

    def do_HEAD(self):
        self._rewrite_tracker_route()
        super().do_HEAD()

    def _rewrite_tracker_route(self):
        raw, _, query = self.path.partition("?")
        if raw != PREFIX and not raw.startswith(PREFIX + "/"):
            return

        suffix = "" if raw in (PREFIX, PREFIX + "/") else raw[len(PREFIX) + 1 :]
        if suffix.endswith("/"):
            suffix = suffix[:-1]

        candidate = APP / suffix if suffix else APP
        if candidate.is_dir():
            rewritten = f"{PREFIX}/index.html" if not suffix else f"{PREFIX}/{suffix}/index.html"
        elif candidate.is_file():
            return
        elif (APP / f"{suffix}.html").is_file():
            rewritten = f"{PREFIX}/{suffix}.html"
        else:
            not_found = APP / "+not-found.html"
            rewritten = f"{PREFIX}/+not-found.html" if not_found.is_file() else raw

        self.path = rewritten if not query else f"{rewritten}?{query}"


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Serving http://127.0.0.1:8765/")
    server.serve_forever()
