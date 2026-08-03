import http.server
import socketserver
import os
import mimetypes
from urllib.parse import quote, unquote

BASE_DIR = os.getcwd()
routes = {}
CHUNK_SIZE = 1024 * 1024  # default 1MB

def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator

class ExplorerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes:
            response, content_type = routes[self.path]()
            self._send_response(response, content_type)
            return

        decoded_path = unquote(self.path)
        filepath = os.path.join(BASE_DIR, decoded_path.lstrip("/"))

        if os.path.isdir(filepath):
            files = os.listdir(filepath)
            folders = [f for f in files if os.path.isdir(os.path.join(filepath, f))]
            files_only = [f for f in files if os.path.isfile(os.path.join(filepath, f))]
            folders.sort()
            files_only.sort()

            html = f"""
            <html>
            <head>
              <meta charset="utf-8">
              <title>File Explorer</title>
              <style>
                body {{
                  font-family: Arial, sans-serif;
                  background-color: #1e1e1e;
                  color: #f0f0f0;
                  margin: 20px;
                }}
                h2 {{
                  color: #4cafef;
                }}
                ul {{
                  list-style-type: none;
                  padding: 0;
                }}
                li {{
                  margin: 8px 0;
                }}
                a {{
                  text-decoration: none;
                  color: #f0f0f0;
                  padding: 6px 10px;
                  border-radius: 4px;
                  display: inline-block;
                  transition: background 0.2s, color 0.2s;
                }}
                a:hover {{
                  background-color: #4cafef;
                  color: #000;
                }}
              </style>
            </head>
            <body>
              <h2>Explorer: {filepath}</h2>
              <ul>
            """

            for f in folders:
                rel = quote(os.path.join(decoded_path, f).replace("\\", "/"))
                html += f"<li><a href='{rel}/'>📁 {f}/</a></li>"

            for f in files_only:
                rel = quote(os.path.join(decoded_path, f).replace("\\", "/"))
                ext = os.path.splitext(f)[1].lower()
                icon = "📄"
                if ext in [".mp4", ".webm", ".avi"]:
                    icon = "🎬"
                elif ext in [".mp3", ".wav", ".flac"]:
                    icon = "🎵"
                elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
                    icon = "🖼️"
                html += f"<li><a href='{rel}'>{icon} {f}</a></li>"

            html += "</ul></body></html>"
            self._send_response(html, "text/html; charset=utf-8")

        elif os.path.isfile(filepath):
            self._serve_file(filepath)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def _serve_file(self, filepath):
        mime, _ = mimetypes.guess_type(filepath)
        file_size = os.path.getsize(filepath)
        range_header = self.headers.get("Range")

        try:
            if range_header:
                start, end = range_header.replace("bytes=", "").split("-")
                start = int(start) if start else 0
                end = int(end) if end else file_size - 1

                self.send_response(206)
                self.send_header("Content-type", mime or "application/octet-stream")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(end - start + 1))
                self.end_headers()

                with open(filepath, "rb") as f:
                    f.seek(start)
                    remaining = end - start + 1
                    while remaining > 0:
                        data = f.read(min(CHUNK_SIZE, remaining))
                        if not data:
                            break
                        try:
                            self.wfile.write(data)
                        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                            break
                        remaining -= len(data)
            else:
                self.send_response(200)
                self.send_header("Content-type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(file_size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                with open(filepath, "rb") as f:
                    while True:
                        data = f.read(CHUNK_SIZE)
                        if not data:
                            break
                        try:
                            self.wfile.write(data)
                        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                            break
        except Exception as e:
            print(f"Client disconnected while serving {filepath}: {e}")

    def _send_response(self, content, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if isinstance(content, str):
            self.wfile.write(content.encode("utf-8"))
        else:
            self.wfile.write(content)

def run(port=80, directory=None, chunk_size=1024*1024):
    global BASE_DIR, CHUNK_SIZE
    if directory:
        BASE_DIR = directory
    CHUNK_SIZE = chunk_size
    with socketserver.ThreadingTCPServer(("", port), ExplorerHandler) as httpd:
        print(f"Serving Explorer at port {port}, base dir: {BASE_DIR}, chunk size: {CHUNK_SIZE} bytes")
        httpd.serve_forever()
