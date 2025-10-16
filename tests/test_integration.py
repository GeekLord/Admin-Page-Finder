import contextlib
import http.server
import socket
import threading

import pytest

from admin_page_finder.scanner import scan_admin_paths


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b'<a href="/admin/">Admin</a>')
        elif self.path == "/admin/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"ok")
        elif self.path == "/login":
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args, **kwargs):  # quiet
        return


@contextlib.contextmanager
def serve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    addr, port = sock.getsockname()
    sock.close()

    server = http.server.ThreadingHTTPServer((addr, port), Handler)
    th = threading.Thread(target=server.serve_forever, daemon=True)
    th.start()
    try:
        yield f"http://{addr}:{port}", th
    finally:
        server.shutdown()
        th.join(timeout=2)


@pytest.mark.asyncio
async def test_end_to_end_scanner():
    with serve() as (base, _):
        results = await scan_admin_paths(base, ["/admin/", "/login", "/missing"])
    statuses = {r.path: r.status for r in results}
    assert statuses.get("/admin/") == 200
    assert statuses.get("/login") == 302
    assert statuses.get("/missing") == 404
