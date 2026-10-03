"""Servidor local para revisar el sitio: python server.py  →  http://localhost:8000

Sirve la carpeta web/ igual que un hosting estático: cada página tiene su
propia carpeta con index.html y las direcciones desconocidas muestran 404.html.
Puerto alternativo: python server.py 8080
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB = Path(__file__).resolve().parent / "web"
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        pagina = WEB / "404.html"
        if code == 404 and pagina.exists():
            cuerpo = pagina.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(cuerpo)
            return
        super().send_error(code, message, explain)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    print(f"Berea: http://localhost:{PUERTO}  (Ctrl+C para detener)")
    ThreadingHTTPServer(("127.0.0.1", PUERTO), partial(Handler, directory=str(WEB))).serve_forever()
