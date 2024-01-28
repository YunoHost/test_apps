from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import base64


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization")
        if auth:
            auth = auth.replace("Basic ", "")
        user, pwd = base64.b64decode(auth.encode()).decode().split(":") if auth else (None, None)
        self.send_response(200)
        self.end_headers()

        if self.path == "/":
            self.wfile.write("Hello world!\n".encode())
        elif self.path == "/show-auth":
            self.wfile.write(f"User: {user}\n".encode())
            self.wfile.write(f"Pwd: {pwd}\n".encode())


webServer = HTTPServer(("127.0.0.1", int(sys.argv[1])), MyServer)
print("Server started")

try:
    webServer.serve_forever()
except BaseException:
    sys.exit(0)
finally:
    webServer.server_close()
    print("Server stopped.")
