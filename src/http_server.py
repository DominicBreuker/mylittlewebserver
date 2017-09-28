import socket
import time


class HttpServer(object):
    def __init__(self, host, port, queue_size=0):
        self.queue_size = queue_size
        self.socket = self._create_and_bind_socket(host, port)

    def serve(self, request_handler):
        self.request_handler = request_handler
        self._receive_forever()

    def name(self):
        return socket.getfqdn(self.socket.getsockname()[0])

    def port(self):
        return self.socket.getsockname()[1]

    def _create_and_bind_socket(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(self.queue_size)
        return sock

    def _receive_forever(self):
        while True:
            client_connection, client_address = self.socket.accept()
            self._handle_connection(client_connection, client_address)
            client_connection.close()

    def _handle_connection(self, connection, address):
        header, body = HttpRequestParser(connection).parse()
        self._log_request(header, body, address)
        response = self.request_handler(header, body)
        self._send_http_response(connection, response)

    def _log_request(self, header, body, address):
        print("{} from {}:{}"
              .format(header.split("\r\n")[0], address[0], address[1]))

    def _send_http_response(self, connection, response):
        connection.sendall(response)
        # time.sleep(30)


class HttpRequestParser(object):
    def __init__(self, connection, buffer_size=1):
        self.connection = connection
        self.request = b""
        self.header = None
        self.body = None
        self.buffer_size = buffer_size

    def parse(self):
        self.header = self._receive_http_header()
        http_method = self._try_get_http_method()
        content_length = self._try_get_content_length()
        if http_method in ["POST", "PUT"] and content_length is not None:
            self.body = self._receive_http_body(content_length)
        return self.header, self.body

    def _receive_http_header(self):
        while b"\r\n\r\n" not in self.request:
            chunk = self.connection.recv(self.buffer_size)
            self.request = b"".join([self.request, chunk])
        return self.request.split(b"\r\n\r\n")[0].decode("utf-8")

    def _receive_http_body(self, content_length):
        while self._body_not_completely_parsed(content_length):
            chunk = self.connection.recv(self.buffer_size)
            self.request = b"".join([self.request, chunk])
        return self.request.split(b"\r\n\r\n")[1].decode("utf-8")

    def _body_not_completely_parsed(self, content_length):
        header_length = len(self.request.split(b"\r\n\r\n")[0])
        return len(self.request) < content_length + header_length \
            + len(b"\r\n\r\n")

    def _try_get_http_method(self):
        try:
            return self.header.split("\r\n")[0].split(" ")[0]
        except:
            return None

    def _try_get_content_length(self):
        try:
            for line in self.header.split("\r\n"):
                if line.lower().startswith("content-length"):
                    return int(line.split(":")[1])
        except:
            return None


if __name__ == "__main__":
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""

    def webapp(header, body):
        return http_response

    server = HttpServer(host="", port=8080)
    server.serve(webapp)
