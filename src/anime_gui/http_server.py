import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class RangeRequestHandler(SimpleHTTPRequestHandler):
    """HTTP handler with Range request support for video streaming"""

    def log_message(self, format, *args):
        pass  # Silent

    def do_GET(self):
        """Handle GET with Range support"""
        path = self.translate_path(self.path)

        try:
            with open(path, "rb") as f:
                fs = os.fstat(f.fileno())
                file_size = fs.st_size

                range_header = self.headers.get("Range")

                if range_header:
                    try:
                        range_value = range_header.replace("bytes=", "")
                        if "-" in range_value:
                            start, end = range_value.split("-")
                            start = int(start) if start else 0
                            end = int(end) if end else file_size - 1

                            if start >= file_size or end >= file_size:
                                try:
                                    self.send_response(416)
                                    self.end_headers()
                                except BrokenPipeError, ConnectionResetError:
                                    pass
                                return

                            length = end - start + 1

                            try:
                                self.send_response(206)
                                self.send_header("Content-Type", "video/mp4")
                                self.send_header("Content-Length", str(length))
                                self.send_header(
                                    "Content-Range", f"bytes {start}-{end}/{file_size}"
                                )
                                self.send_header("Accept-Ranges", "bytes")
                                self.end_headers()

                                f.seek(start)
                                self.wfile.write(f.read(length))
                            except BrokenPipeError, ConnectionResetError:
                                pass
                            return
                    except:
                        pass

                # No range request, send full file
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "video/mp4")
                    self.send_header("Content-Length", str(file_size))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()

                    self.wfile.write(f.read())
                except BrokenPipeError, ConnectionResetError:
                    pass
        except FileNotFoundError:
            try:
                self.send_response(404)
                self.end_headers()
            except BrokenPipeError, ConnectionResetError:
                pass
        except Exception:
            try:
                self.send_response(500)
                self.end_headers()
            except BrokenPipeError, ConnectionResetError:
                pass


def start_sever(resource_dir: Path) -> HTTPServer:
    """Start HTTP server with range request support"""
    os.chdir(resource_dir)

    http_server = HTTPServer(("localhost", 8765), RangeRequestHandler)
    thread = threading.Thread(target=http_server.serve_forever, daemon=True)
    thread.start()
    print(f"HTTP server started: {resource_dir}")

    return http_server
