import logging
import socketserver
import ssl
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        logging.info(query_params)
        if "code" in query_params:
            authorization_code = query_params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(
                    f"<html><body><h4>Authorization successful. You can now close this window, your code is: </h4><h1>{authorization_code}</h1> </body></html>",
                    "utf-8",
                )
            )
            raise KeyboardInterrupt
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes("<html><body<h1>Bad request</h1></body></html>", "utf-8")
            )


def run_callback_server(click):
    host = "localhost"
    port = 3000

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("bin/server.pem")

    server_address = (host, port)

    with socketserver.TCPServer(server_address, CallbackHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        click.echo(f"- Starting server on {host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
