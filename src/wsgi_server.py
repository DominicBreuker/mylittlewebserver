import os
import sys
from io import StringIO
from datetime import datetime

from http_server import HttpServer
from http_fork_server import HttpForkServer


class WsgiServer(object):
    def __init__(self, host, port, fork=True):
        self.server = self._create_server(host, port, fork)
        self.server_name = self.server.name()
        self.server_port = self.server.port()

    def _create_server(self, host, port, fork):
        if fork:
            return HttpForkServer(host=host, port=port)
        else:
            return HttpServer(host=host, port=port)

    def serve(self, application):
        self.application = application
        self.server.serve(self._request_handler)

    def _request_handler(self, header, body):
        env = WsgiRequestParser(header, body, self).get_environ()
        return WsgiResponse(env, self.application).create()


class WsgiRequestParser(object):
    def __init__(self, header, body, wsgi_server):
        self.header = header
        self.body = body
        self.wsgi_server = wsgi_server

    def get_environ(self):
        method, path, version = self._parse_request_line()
        env = dict(os.environ.items())
        env["wsgi.version"] = (1, 0)
        env["wsgi.url_scheme"] = "http"
        env["wsgi.input"] = self._request_data()
        env["wsgi.errors"] = sys.stderr
        env["wsgi.multithread"] = False
        env["wsgi.multiprocess"] = False
        env["wsgi.run_once"] = False
        env["REQUEST_METHOD"] = method
        env["PATH_INFO"] = path
        env["SERVER_NAME"] = self.wsgi_server.server_name
        env["SERVER_PORT"] = str(self.wsgi_server.server_port)
        return env

    def _parse_request_line(self):
        return self.header.splitlines()[0].rstrip("\r\n").split(" ")

    def _request_data(self):
        try:
            return StringIO(self.body)
        except:
            return StringIO("")


class WsgiResponse(object):
    def __init__(self, env, application):
        self.env = env
        self.application = application

    def create(self):
        try:
            self.app_response = self.application(self.env,
                                                 self._start_response)
            header = self._format_header()
            body = self._format_body()
            return header + body
        except:
            return "HTTP/1.1 500 Internal Error\r\n\r\n"

    def _start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', datetime.now().isoformat(' ')),
            ('Server', 'MyWSGIServer 1.0'),
        ]
        self.status = status
        self.headers = response_headers + server_headers

    def _format_header(self):
        header = "HTTP/1.1 {}\r\n".format(self.status)
        for key, value in self.headers:
            header += '{}: {}\r\n'.format(key, value)
        header += "\r\n"
        return header.encode("utf-8")

    def _format_body(self):
        return b"".join([data for data in self.app_response])


if __name__ == "__main__":
    server = WsgiServer("", 8080)

    def application(env, start_response):
        start_response("200 OK", [("X-IMPORTANT-INFO", "hello world")])
        return [b"Hello, World from the WSGI App!\n"]

    server.serve(application)
