"""Servidor local para ver as apostilas (sem cache, para enxergar cada edição na hora).

Uso:  python scripts/serve.py [porta]      (padrão: 4323)
Depois abra http://localhost:4323
"""
import http.server
import os
import sys

PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 4323
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(RAIZ)


class SemCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


http.server.ThreadingHTTPServer.allow_reuse_address = True
with http.server.ThreadingHTTPServer(("", PORTA), SemCache) as srv:
    print(f"Apostilas em http://localhost:{PORTA}  (Ctrl+C para parar)")
    srv.serve_forever()
