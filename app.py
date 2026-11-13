from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def read_status():
    return Path(__file__).with_name("status.txt").read_text(
        encoding="utf-8"
    ).strip()


def is_healthy(status):
    return status == "status=HEALTHY"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/status":
            self.send_error(404)
            return

        status = read_status()
        code = 200 if is_healthy(status) else 503
        payload = (status + "\n").encode("utf-8")

        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    server.serve_forever()
